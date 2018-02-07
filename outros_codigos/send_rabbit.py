from threading import Thread
import time
import paho.mqtt.client as mqtt
import ntplib

mqttc = mqtt.Client()
mqttc.username_pw_set("psd", "psd")
mqttc.connect("192.168.25.50", 1883)


dicionario_segundos = {}

with open("contagem.txt") as arquivo:
    for linha in arquivo:
        linha = linha.split(" ")
        timestamp = int(linha[2])
        rssi = int(linha[1])
        mac = linha[0]
        if timestamp not in dicionario_segundos:
            dicionario_segundos[timestamp] = [(mac,rssi)]
        elif mac not in dicionario_segundos[timestamp]:
            dicionario_segundos[timestamp].append((mac,rssi))

antes = int(time.time()) + 0

ntp = ntplib.NTPClient()
resposta = ntp.request("pool.ntp.org")
timestamp_atual = int(resposta.recv_time)
timestamp_antigo = 1516185697

def worker(timestamp_antigo, timestamp_atual):
    if timestamp_antigo in dicionario_segundos.keys():
        lista = dicionario_segundos[timestamp_antigo]
        for i in lista:
            mqttc.publish("hello", "{} {} {}p".format(i[0], i[1], timestamp_atual))
            print("mandei {} {} {}p".format(i[0], i[1], timestamp_atual))


while True:
    agora = time.time()
    if int(agora) == int(antes) + 1:
        antes = time.time()
        Thread(target=worker,args=[timestamp_antigo, timestamp_atual]).start()
        timestamp_atual += 1
        timestamp_antigo += 1
    elif int(agora) > int(antes) +1:
        print("------------------------------------------")
        print("------------------------------------------")
        print("lentidão no processamento")
        print("------------------------------------------")
        print("------------------------------------------")
        break
