from models import *
from flask import Flask
from flask_restful import Api
from load_database import carregar_arquivo_no_banco, processa_lista_de_filmes_e_transforma_em_produtores
from defines import path_arquivo_importacao

app = Flask(__name__)
api = Api(app)

try:
    carregar_arquivo_no_banco(path_arquivo_importacao)
except Exception as e:
    print(f"Houve um problema ao inserir arquivo banco: -> \n {e}")


@app.route('/')
def encontra_filmes():
    dict_processamento = processa_lista_de_filmes_e_transforma_em_produtores()
    return dict_processamento


if __name__ == '__main__':
    app.run(debug=True)
