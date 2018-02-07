#!flask/bin/python
from flask import Flask, jsonify, abort
import time
from threading import Thread, Lock
import urllib.request
import ntplib

IP_Bernardo = "192.168.25.50"
IP_Ariana = "192.168.48.1"
IP = IP_Ariana


ntp = ntplib.NTPClient()


macs = {}

def adicionar_dicionario(dicionario,lista,mac = None, sinal = None, time_stamp_ativo = None, time_stamp_presente = None):
    dicionario[lista[0]] = [lista[0],lista[1],lista[2],lista[3],"p"]

def atualizar_dicionario(dicionario, lista, mac = None, sinal = None, time_stamp_ativo = None):
    dicionario[lista[0]][1] = lista[1]
    dicionario[lista[0]][2] = lista[2]

mutex_dicionario = Lock()


app = Flask(__name__)

@app.route('/')
def index():
    return "Service Funcionando!"


@app.route('/circular/<string:novo_mac>', methods=['GET'])
def get_task(novo_mac):
    if len(novo_mac) == 0:
        abort(404)
    Thread(target=send_mac, args=[novo_mac]).start()
    conta(novo_mac)
    return jsonify({'ok': "mac-recebido"})


def conta_lotacao(timestamp,dicionario):
    lotacao = 0
    for i in dicionario.keys():
        if dicionario[i][4] == str("a"):
            lotacao += 1
    mensagem = str(lotacao) + "%20" + str(timestamp)
    print("{} dentro do circular em {}".format(lotacao, timestamp))
    content = urllib.request.urlopen("http://" + IP + ":5001/att-lotacao/" + mensagem).read()


def send_mac(mensagem):
    mensagem = mensagem.replace(" ","%20")
    content = urllib.request.urlopen("http://" + IP + ":5001/add-mac/" + mensagem).read()


def conta(mensagem):
    global macs
    mensagem = mensagem.split(" ")
    mac = mensagem[0]
    sinal = mensagem[1]
    time_stamp = mensagem[2]
    # mac_n = Mac(mac,sinal,time_stamp,time_stamp,"p")
    mac_n = [mac,sinal,time_stamp,time_stamp]
    # Thread(target=gateway, args=[mac_n, mutex_dicionario, macs]).start()
    gateway(mac_n, mutex_dicionario, macs)

cache_gateway = []

def gateway(lista_mac, mutex, dicionario):

    if mutex.locked():
        print("Mutex is locked")
        cache_gateway.append(lista_mac)
    else:
        mutex.acquire()
        try:
            for i in cache_gateway:
                dicionario_funcoes(i, dicionario)
            cache_gateway.clear()
            dicionario_funcoes(lista_mac, dicionario)
        finally:
            mutex.release()

def dicionario_funcoes(lista_mac, dicionario):
    if lista_mac[0] not in dicionario.keys():
        adicionar_dicionario(dicionario,lista_mac)
    else:
        atualizar_dicionario(dicionario,lista_mac)

def worker(timestamp, dicionario, tempo_vida_ativo, tempo_vida_presente = 60):
    dicionario_keys = []
    for j in dicionario.keys():
        dicionario_keys.append(j)
    for i in dicionario_keys:
        if (int(dicionario[i][2]) + tempo_vida_ativo) < timestamp:
            del dicionario[i]
        elif int(dicionario[i][3]) + int(tempo_vida_presente) < timestamp:
            dicionario[i][4] = "a"

def sub_main_thread(dict, mutex, tempo_atual):
    timestamp_atual = tempo_atual
    while True:
        antes = time.time()
        if not mutex.locked():
            mutex.acquire()
            try:
                worker(timestamp_atual, dict, 90, 80)
            finally:
                mutex.release()
        Thread(target=conta_lotacao,args=(timestamp_atual, dict)).start()
        agora = time.time()
        slp = (antes + 1) - agora
        time.sleep(slp)
        timestamp_atual += 1


if __name__ == '__main__':
    while True:
        try:
            resposta = ntp.request("pool.ntp.org")
            hora_atual = int(resposta.recv_time)
        finally:
            break
    Thread(target=sub_main_thread, args=[macs, mutex_dicionario, hora_atual]).start()
    app.run(host="0.0.0.0", port=5000)
