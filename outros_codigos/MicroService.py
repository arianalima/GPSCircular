#!flask/bin/python
from flask import Flask, jsonify, abort

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"



@app.route('/circular/<string:macs>', methods=['GET'])
def get_task(macs):
    if len(macs) == 0:
        abort(404)
    print(macs)
    return jsonify({'ok': "nok"})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

def conta(mensagem):
    mensagem = mensagem.split(" ")
    mac = mensagem[0]

    pass

def conta_unfiltered(mensagem):
    pass

def conta_90(mensagem):
    pass

def conta_150(mensagem):
    pass

def conta_180(mensagem):
    pass