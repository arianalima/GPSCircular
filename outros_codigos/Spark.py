import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from mqtt import MQTTUtils
import threading
import time
import urllib2

IP_Bernardo = ""
IP_Ariana = "192.168.48.1"
IP = IP_Ariana

macs = {}
n = []
def unico(line):
    if line[0] not in n:
        n.append(line[0])
        return line[0]

def atualiza_dicionario(macs):
    while True:
        quantidade = 0
        try:
            timestamp_atual = int(time.time())
            for mac, mac_tuple in macs.iteritems():
                timestamp_limite_ativo = int(mac_tuple[1])
                timestamp_limite_recente = int(mac_tuple[0])
                if timestamp_atual > timestamp_limite_ativo:
                    macs.pop(mac, None)
                elif(timestamp_limite_recente < timestamp_atual):
                    quantidade += 1
        except Exception as e:
            print("erro na thread atualiza_dicionario " + str(e))

threading.Thread(target=atualiza_dicionario,args=macs)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: mqtt_wordcount.py <broker url> <topic>"
        exit(-1)

    sc = SparkContext(appName="PythonStreamingMQTTWordCount")
    ssc = StreamingContext(sc, 10)

    brokerUrl = sys.argv[1]
    topic = sys.argv[2]

    lines = MQTTUtils.createStream(ssc, brokerUrl, topic)
    #counts = lines.flatMap(lambda line: line.split(" ")) \
    #    .map(lambda word: (word, 1)) \
    #    .reduceByKey(lambda a, b: a+b)

    
    #linhas = lines.filter(lambda lines: lines.split("\n"))
    
    def reduceTupla(t1,t2):
        ts1 = t1[1]
        ts2 = t2[1]
        if ts1 >= ts2:
            return t1
        else:
            return t2
    
    linhas = lines.map(lambda line: line.split(" "))\
                .map(lambda line: (line[0],(line[1],int(line[2][:-1]))))\
                .reduceByKey(reduceTupla)
                
    def send(message):
        try:
            txt_message = str(message[0]) +"%20"+ str(message[1][0]) +"%20"+ str(message[1][1])
            urllib2.urlopen("http://"+IP+":5000/circular/" + txt_message).read()
            print(message)
        except:
            print"HTPP error"
    
        
    linhas.foreachRDD(lambda p: p.foreach(send))
    #counts.pprint()

    ssc.start()
ssc.awaitTermination()
