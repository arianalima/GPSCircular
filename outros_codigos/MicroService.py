#!flask/bin/python
from flask import Flask, jsonify, abort

class Mac():
    def __init__(self, mac, sinal, time_stamp_ativo, time_stamp_presente, flag):
        self.mac = mac
        self.sinal = sinal
        self.time_stamp_ativo = time_stamp_ativo
        self.time_stamp_presente = time_stamp_presente
        self.flag = flag

    def adicionar_em_dicionario(self, dicionario):
        dicionario[self.mac] = self

    def atualizar_dicionario(self, dicionario):
        dicionario[self.mac].time_stamp_ativo = self.time_stamp_ativo



macs_unfiltered = {}
macs_90 = {}
macs_150 = {}
macs_180 = {}

# flag: p de presente, a ativo
# mac_exemplo = {"mac":"12:55:d4:66:88", "sinal":-50, "time_stamp_ativo":1212333456787, "time_stamp_presente":1212333456789, "flag":"p"}

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"



@app.route('/circular/<string:novo_mac>', methods=['GET'])
def get_task(novo_mac):
    if len(novo_mac) == 0:
        abort(404)
    print("novo MAC recebido : {}".format(novo_mac))
    conta(novo_mac)
    return jsonify({'ok': "mac-recebido"})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

def conta(mensagem):
    mensagem = mensagem.split(" ")
    mac = mensagem[0]
    sinal = mensagem[1]
    time_stamp = mensagem[2]
    mac_n = Mac(mac,sinal,time_stamp,time_stamp,"p")
    gateway(mac_n, macs_unfiltered)
    gateway(mac_n, macs_90)
    gateway(mac_n, macs_150)
    gateway(mac_n, macs_180)

def gateway(objeto_mac, dicionario):
    if objeto_mac.mac not in dicionario.keys():
        objeto_mac.adicionar_em_dicionario(dicionario)
    else:
        objeto_mac.atualizar_dicionario(dicionario)
