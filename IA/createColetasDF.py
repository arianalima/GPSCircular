from datetime import timedelta, datetime
from csv import reader
QTD_COLETAS = 30
TEMPO_PRESENTE = 80
TEMPO_ATIVO = 90
resultados = []

f = open('df_coletas_p{}a{}.arff'.format(TEMPO_PRESENTE,TEMPO_ATIVO),'w')
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
    if lotacao_real > 43:
        return "superlotado"
    elif 43 >= lotacao_real >= 33:
        return "lotado"
    elif 33 > lotacao_real >= 23:
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
        data = data[TEMPO_PRESENTE + 1:]
        list(map(lambda line: f.write(str(coleta)+",")
                              and list(map(lambda var: f.write(var+","), line))
                              and f.write(getClassification(int(line[4])))
                              and f.write("\n")
                              and resultados.append((coleta,getClassification(int(line[4])),getClassification(int(line[1])))),data))
        file.close()

list(map(lambda x: read(x),range(1,QTD_COLETAS+1)))

f.close()

def countError(classe):
    expected = sum(map(lambda tuple: tuple[1].count(classe), resultados))
    reality = sum(map(lambda tuple: tuple[2].count(classe), resultados))
    return expected-reality


total = len(resultados)
vazio = countError('vazio')
normal = countError('normal')
lotado = countError('lotado')
superlotado = countError('superlotado')
