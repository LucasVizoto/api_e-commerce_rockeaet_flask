from flask import Flask

app = Flask(__name__)
#isso instancia o aplicativo do flask

#-------------ROTAS------------#
# definir uma rota raiz, ou seja, da página inicial
# e a função que será executada quando um usuário requisitar

@app.route('/') #aqui eu defino a "home" da API
def hello_world() -> str: #
    return 'Hello World'

if __name__== "__main__":
    app.run(debug=True)
    #debug=True é só em ambiente de desenvolvimento e nunca deve estar em prod
