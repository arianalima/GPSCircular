from threading import Thread
import time

dicionario_segundos = {}

with open("contagem.txt") as arquivo:
    for linha in arquivo:
        timestamp = int(linha.split(" ")[2])
        mac = linha.split(" ")[0]
        if timestamp not in dicionario_segundos:
            dicionario_segundos[timestamp] = [mac]
        elif mac not in dicionario_segundos[timestamp]:
            dicionario_segundos[timestamp].append(mac)

antes = int(time.time()) + 0

timestamp_atual = 1516185697

def worker(timestamp):
    if timestamp in dicionario_segundos.keys():
        lista = dicionario_segundos[timestamp]
        print("macs {}".format(lista))

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







