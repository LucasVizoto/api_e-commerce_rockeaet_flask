from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#isso instancia o aplicativo do flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
#linha de início do banco
db = SQLAlchemy(app)
#--------------MODELAGEM-------------#
# Molde de linhas e colunas que vou definir pro meu banco
# Produto [id,name, price, description]

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#-------------ROTAS------------#
# definir uma rota raiz, ou seja, da página inicial
# e a função que será executada quando um usuário requisitar

@app.route('/api/products/add', methods=["POST"])
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


