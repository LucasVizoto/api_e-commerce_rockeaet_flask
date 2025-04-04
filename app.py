from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
app = Flask(__name__)
#isso instancia o aplicativo do flask
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
#linha de início do banco
login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)
# pra testar no swagger ao invés do insomnia ou postman

#--------------MODELAGEM-------------#
# Molde de linhas e colunas que vou definir pro meu banco
# Produto [id,name, price, description]
class User(db.Model, UserMixin,):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)

# No Flask Shell, dropei tudo pra criar tudo de novo Flask migrate
# incrimentar o banco sem perder os registros
# >>> db.drop_all()
# >>> db.create_all()
# >>> db.session.commit()
# >>> exit()

#adicionando usuário
# >>> user = User(username="admin", password="123")
# >>> user
# <User (transient 2130592974368)>
# >>> user.id
# >>> db.session.add(user)
# >>> db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#-------------ROTAS------------#
# definir uma rota raiz, ou seja, da página inicial
# e a função que será executada quando um usuário requisitar
#Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    # basicamente estou filtrando no banco os usuários pelo username e pegando o primeiro
    if user and data.get("password") == user.password: # verificando se o usuário existe se a senha condiz com o que foi eviado
        login_user(user)
        return jsonify({"message":"Logged in successfully"}), 200
    return jsonify({"message":"Unouthorized. Invalid credential"}), 401

@app.route('/logout', methods=['POST'])
@login_required #caso eu tente dar logout de novo ele lança 405, método não permitido
def logout():
    logout_user()
    return jsonify({"message":"Logged out successfully"}), 200


@app.route('/api/products/add', methods=["POST"])
@login_required #só precisa disso pra dizer que a rota só é acessível caso logado
def add_product():
    data = request.json #request importado do Flask faz com que eu tenha acesso à todos os dados da requisição
    if 'name' in data and 'price' in data: # verifico se as chaves name e price estão em data
        product = Product(name=data["name"],price=data["price"],description=data.get("description", "")) 
        # o get faz uma espécie de Coalesce ou NVL com o que for passado, se tiver, faz oq está em primeiro, caso contrário o segundo
        db.session.add(product) #fiz o insert no banco
        db.session.commit()
        return jsonify({"message":"Product added successfully"}), 200
    return jsonify({"message":"Invalid product data"}), 400
# tudo que a API retorna precisa ser em JSON, por isso é feita essa tratativa
# o segundo valor é referente à response http que esse endpoint vai retornar

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    #Recuperar o produto da base de dados
    # verificar se existe se existe apagar
    # se não Not Found 404
    product = Product.query.get(product_id) #fiz basicamente um find by ID
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"}), 200
    return jsonify({"message":"Product not found"}), 404

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id":product.id,
            "name":product.name,
            "price": product.price,
            "description":product.description            
        }), 200
    return jsonify({"message":"Product not found"}), 404
  
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product: # se não tem produto ele entra aqui direto
        return jsonify({"message": "Product not found"}), 404
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    
    return jsonify({"message": "Product updated successfully"}), 200  


@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = ({
            "id":product.id,
            "name":product.name,
            "price": product.price,         
        })
        product_list.append(product_data)
    return jsonify(product_list), 200



#definir uma rota raiz e a função qeu será executada ao requisitar
@app.route('/') #aqui eu defino a "home" da API
def hello_world() -> str: #
    return 'Hello World'

@app.shell_context_processor
def make_shell_context() -> dict:
    return {'db': db, 'Product': Product}


if __name__== "__main__":
    app.run(debug=True)
    #debug=True é só em ambiente de desenvolvimento e nunca deve estar em prod
    #o debug basicamente mostra as informações de todas as requisições que baterão aqui


