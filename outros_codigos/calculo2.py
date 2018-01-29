import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from mqtt import MQTTUtils
import threading
import time

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
                elif (timestamp_limite_recente < timestamp_atual):
                    quantidade += 1
        except Exception as e:
            print("erro na thread atualiza_dicionario " + str(e))


threading.Thread(target=atualiza_dicionario, args=macs)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: mqtt_wordcount.py <broker url> <topic>"
        exit(-1)

    sc = SparkContext(appName="PythonStreamingMQTTWordCount")
    ssc = StreamingContext(sc, 10)

    brokerUrl = sys.argv[1]
    topic = sys.argv[2]

    lines = MQTTUtils.createStream(ssc, brokerUrl, topic)
    # counts = lines.flatMap(lambda line: line.split(" ")) \
    #    .map(lambda word: (word, 1)) \
    #    .reduceByKey(lambda a, b: a+b)

    # linhas = lines.filter(lambda lines: lines.split("\n"))
    linhas = lines.map(lambda line: line.split(" ")) \
        .map(lambda line: (line[0], int(line[2][:-1]))) \
        .reduceByKey(lambda ts1, ts2: max(ts1, ts2))


    def send(p):
        print(p)


    linhas.foreachRDD(lambda p: p.foreach(send))
    # counts.pprint()

    ssc.start()
ssc.awaitTermination()