from datetime import timedelta, datetime
from csv import reader
QTD_COLETAS = 25
TEMPO_PRESENTE = 80
TEMPO_ATIVO = 90

f = open('df_coletas.arff','w')
f.write("@relation df_coletas\n\n"
        "@attribute coleta integer\n"
        "@attribute segundo_coleta integer\n"
        "@attribute lotacao integer\n"
        "@attribute total_segundos integer\n"
        "@attribute hora string\n"
        "@attribute lotacao_real integer\n"
        "@attribute temp_aparente numeric\n"
        "@attribute precipitacao numeric\n"
        "@attribute class {vazio, normal, lotado, superlotado}\n\n"
        "@data\n")

def getWeekDay(timestamp):
    return str(datetime.fromtimestamp(int(timestamp)).weekday())

def getClassification(lotacao_real):
    if lotacao_real > 33:
        return "superlotado"
    elif 33 >= lotacao_real >= 23:
        return "lotado"
    elif 23 > lotacao_real >= 13:
        return "normal"
    else:
        return "vazio"

def getSecsTotal(timestamp):
    return str(timedelta(seconds=int(timestamp)).seconds)

def changeTsSecsTotal(index, value, list):
    list[index][2] = value

def read(coleta):
    with open ("..\\Coletas\\csv's\\coleta " + str(coleta) + " algoritmo p" + str(TEMPO_PRESENTE) + \
                   " a" + str(TEMPO_ATIVO) + ".csv") as file:
        data = list(map(lambda line:line,reader(file)))
        header = data.pop(0)
        list(map(lambda index:
                 changeTsSecsTotal(index, getSecsTotal(data[index][2]), data), range(len(data))))
        data = list(filter(lambda line: line[1]!='0', data))

        list(map(lambda line: f.write(str(coleta)+",")
                              and list(map(lambda var: f.write(var+","), line))
                              and f.write(getClassification(int(line[4])))
                              and f.write("\n"),data))

        file.close()

list(map(lambda x: read(x),range(1,QTD_COLETAS+1)))

f.close()
