from threading import Thread
import time
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.username_pw_set("psd", "psd")
mqttc.connect("10.246.42.39", 1883)


dicionario_segundos = {}

with open("coleta1.txt") as arquivo:
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

timestamp_atual = 1516185697

def worker(timestamp):
    if timestamp in dicionario_segundos.keys():
        lista = dicionario_segundos[timestamp]
        for i in lista:
            mqttc.publish("hello", "{} {} {}p".format(i[0], i[1], timestamp))
            print("mandei {} {} {}p".format(i[0], i[1], timestamp))

while True:
    agora = time.time()
    if int(agora) == int(antes) + 1:
        antes = time.time()
        Thread(target=worker,args=[timestamp_atual]).start()
        timestamp_atual += 1
    elif int(agora) > int(antes) +1:
        print("------------------------------------------")
        print("------------------------------------------")
        print("lentidão no processamento")
        print("------------------------------------------")
        print("------------------------------------------")
        break







