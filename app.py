from models import *
from flask import Flask, jsonify
from flask_restful import Api
from load_database import carregar_arquivo_no_banco, processa_lista_de_filmes_e_transforma_em_produtores
from defines import path_arquivo_importacao
from flask_caching import Cache

app = Flask(__name__)
api = Api(app)
# configurando cache para ser mais rápido a resposta para usuario uma vez que a api é 'estática'
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)

try:
    carregar_arquivo_no_banco(path_arquivo_importacao)
except Exception as e:
    print(f"Houve um problema ao inserir arquivo banco: -> \n {e}")


@app.route('/producers', methods=['GET'])
@cache.cached()
def encontra_filmes():
    dict_processamento = processa_lista_de_filmes_e_transforma_em_produtores()
    return jsonify(dict_processamento), 200


@app.errorhandler(500)
def handle_500_error(error):
    response = {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred on the server."
    }
    return jsonify(response), 500


@app.errorhandler(404)
def url_nao_econtrada(error):
    return jsonify({"error": "URL não encontrada!"}), 404


if __name__ == '__main__':
    app.run()
