#!flask/bin/python

import os
from flask import Flask, jsonify, make_response

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

@app.route('/circular/get/localizacao', methods=['GET'])
def get_posicao():
    return jsonify({'result': "posicao 123097128037182093"})

@app.route('/circular/get/lotacao', methods=['GET'])
def get_lotacao():
    return jsonify({'result': "tem 123097128037182093 pessoas"})


if __name__ == '__main__':
    app.run(debug=True)