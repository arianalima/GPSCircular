#!flask/bin/python

import os
from flask import Flask, jsonify, make_response
import Database as db

app = Flask(__name__, static_url_path="")



@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def get_home():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "template/home.html"
    abs_file_path = os.path.join(script_dir, rel_path)
    arq = open(abs_file_path,"r")
    texto = arq.read()
    return texto


@app.route('/add-mac/<string:mensagem>', methods=['GET'])
def add_mac(mensagem):
    try:
        lista_mensagem = mensagem.split(" ")
        mac = lista_mensagem[0]
        sinal = lista_mensagem[1]
        time_stamp = lista_mensagem[2]
        db.inserirPessoa(mac,int(sinal),int(time_stamp))
    except:
        return "nok"
    return "ok"

@app.route('/circular/get/localizacao', methods=['GET'])
def get_posicao():
    return jsonify({'resultado': "posicao 1230971280 37182093"})

@app.route('/circular/get/lotacao', methods=['GET'])
def get_lotacao():
    return jsonify({'resultado': "tem 123097128037182093 pessoas"})


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0',port=5001)