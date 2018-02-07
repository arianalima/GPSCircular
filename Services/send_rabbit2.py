from threading import Thread
import time
# import paho.mqtt.client as mqtt

# mqttc = mqtt.Client()
# mqttc.username_pw_set("psd", "psd")
# mqttc.connect("192.168.25.50", 1883)

dicionario_90 = {}
dicionario_150 = {}
dicionario_180 = {}

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

timestamp_inicial = 1516185697
timestamp_atual = 1516185697

def worker(timestamp,dicionario):
    if timestamp in dicionario_segundos.keys():
        lista = dicionario_segundos[timestamp]
        for i in lista:
            # mqttc.publish("hello", "{} {} {}p".format(i[0], i[1], timestamp))
            mac_n = Mac(i[0], i[1], timestamp, timestamp, "p")
            adiciona_dicionario(mac_n,dicionario)
            # print("mandei {} {} {}p".format(i[0], i[1], timestamp))

def adiciona_dicionario(objeto_mac, dicionario):
    if objeto_mac.mac not in dicionario.keys():
        objeto_mac.adicionar_em_dicionario(dicionario)
        # print("adicionou mac {} em um dicionario".format(objeto_mac.mac))
    else:
        objeto_mac.atualizar_dicionario(dicionario)
global a
a=True
def vigia_dicionario(timestamp, dicionario, tempo_vida_ativo, tempo_vida_presente = 60):
    timestp_ativo_final = timestamp + tempo_vida_ativo
    dicionario_keys = []
    for j in dicionario.keys():
        dicionario_keys.append(j)

    for i in dicionario_keys:
        if (int(dicionario[i].time_stamp_ativo) + tempo_vida_ativo) < timestamp:
            del dicionario[i]
        elif int(dicionario[i].time_stamp_presente + tempo_vida_presente) < timestamp:
            dicionario[i].flag = "a"
    contador = 0
    for i in dicionario.keys():
        if dicionario[i].flag == "a":
            contador+=1

    segundo = timestamp - timestamp_inicial
    arquivo = open("log_dicionario" + str(tempo_vida_ativo) + ".txt","a")
    # arquivo.write(str(segundo) + "\t" + str(contador) + "\n")

    arquivo.write(str(contador) + "\n")
    if contador == 0 and segundo>1000:
        a = False
    print(str(segundo) + "," + str(len(dicionario.keys())))
    arquivo.close()

while True:
    if a ==True:

        # agora = time.time()
        # if int(agora) == int(antes) + 1:
            # antes = time.time()
        worker(timestamp_atual,dicionario_150)
        #80, 70
        vigia_dicionario(timestamp_atual,dicionario_150,90,tempo_vida_presente=80)
        timestamp_atual += 1
        # elif int(agora) > int(antes) +1:
        #     print("------------------------------------------")
        #     print("------------------------------------------")
        #     print("lentidão no processamento")
        #     print("------------------------------------------")
        #     print("------------------------------------------")
    else:
        break