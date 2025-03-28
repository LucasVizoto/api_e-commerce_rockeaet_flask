from flask import Flask, request
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
    return data

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


