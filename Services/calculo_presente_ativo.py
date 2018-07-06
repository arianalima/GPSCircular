import os
import datetime

PRESENTE = "p"
ATIVO = "a"

class Mac:
    def __init__(self, mac, sinal, time_stamp_ativo, time_stamp_presente, flag = PRESENTE):
        self.__mac = mac
        self.__sinal = sinal
        self.__time_stamp_ativo = time_stamp_ativo
        self.__time_stamp_presente = time_stamp_presente
        self.__flag = flag

    def get_mac(self):
        return self.__mac

    def get_time_ativo(self):
        return self.__time_stamp_ativo

    def get_time_presente(self):
        return self.__time_stamp_presente

    def atualizar_dicionario(self, timestamp):
        self.__time_stamp_ativo = timestamp

    def set_modo_ativo(self):
        self.__flag = ATIVO

    def is_ativo(self):
        if self.__flag == ATIVO:
            return True


def add_linha_dicionario(linha):
    linha = linha[:-1]
    linha = linha.split()
    timestamp = int(linha[2])
    rssi = int(linha[1])
    mac = linha[0]
    if timestamp not in dicionario_segundos:
        dicionario_segundos[timestamp] = {}
    if mac not in dicionario_segundos[timestamp]:
        dicionario_segundos[timestamp][mac] = rssi
    elif abs(dicionario_segundos[timestamp][mac]) < abs(rssi):
        dicionario_segundos[timestamp][mac] = rssi

# with open("coleta1.txt") as arquivo:
#     def create_dic_data(timestamp, rssi, mac, dictionary):
#         if timestamp not in dictionary:
#             dictionary[timestamp] = {}
#         if mac not in dictionary[timestamp]:
#             dictionary[timestamp][mac] = rssi
#         elif abs(dictionary[timestamp][mac]) < abs(rssi):
#             dictionary[timestamp][mac] = rssi
#
#     def process_file(file_read, dictionary):
#         processed_lines = list(map(lambda x: x.replace("Log: ", "").split(), file_read))
#         list(map(lambda x: create_dic_data(x[2], int(x[1]), x[0], dictionary), processed_lines))
#         return dictionary
#
#     process_file(arquivo, dicionario_segundos)

def worker(timestamp, dicionario):
    if timestamp in dicionario_segundos.keys():
        sub_dicionario = dicionario_segundos[timestamp]
        list(map(adiciona_dicionario(timestamp, sub_dicionario, dicionario), sub_dicionario.keys()))

def adiciona_dicionario(timestamp, sub_dicionario, dicionario):
    def run_adiciona_dicionario(item_mac):
        mac = item_mac
        sinal = sub_dicionario[item_mac]
        objeto_mac = Mac(mac, sinal, timestamp, timestamp, PRESENTE)
        if objeto_mac.get_mac() not in dicionario.keys():
            dicionario[mac] = objeto_mac
        else:
            dicionario[mac].atualizar_dicionario(timestamp)
    return run_adiciona_dicionario

def vigia_dicionario(timestamp, dicionario, tempo_vida_ativo, tempo_vida_presente = 60):

    def att_dicionario(mac):
        if int(dicionario[mac].get_time_ativo() + tempo_vida_ativo) < timestamp:
            del dicionario[mac]
        elif int(dicionario[mac].get_time_presente() + tempo_vida_presente) < timestamp:
            dicionario[mac].set_modo_ativo()

    list(map(att_dicionario, list(dicionario.copy())))

    lista_ativos = list(filter(lambda x: dicionario[x].is_ativo(), dicionario.keys()))
    contador = len(lista_ativos)

    return contador


def criar_cabecalho(coleta, presente, ativo):
    path_arquivo = "..\\Coletas\\coleta "+ str(coleta) +" algoritmo p" + str(presente) + \
              " a" + str(ativo) + ".csv"

    arquivo = open(path_arquivo, "a")
    arquivo.write("segundo,calculo,timestamp,hora_minuto,valor_real" + "\n")
    arquivo.close()

def get_texto_hora(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    minuto = time.minute
    hora = (time.hour + 3)
    texto_hora = "{}:{}".format(str(hora), str(minuto).rjust(2, "0"))
    return texto_hora

def set_valor_real(ultimo_valor, dicionario_valor, texto_hora):
    if (texto_hora in dicionario_valor):
        ultimo_valor = dicionario_valor[texto_hora]

def salvar_em_arquivo(contagem, coleta, presente, ativo, segundo, timestamp,texto_hora, ultimo_valor):

    path_arquivo = "..\\Coletas\\coleta " + str(coleta) + " algoritmo p" + str(presente) + \
                   " a" + str(ativo) + ".csv"

    arquivo = open(path_arquivo, "a")
    arquivo.write("{},{},{},{},{}".format(str(segundo),str(contagem),str(timestamp),texto_hora,ultimo_valor) + "\n")
    arquivo.close()

def add_dicionario_coleta_real(dicionario):
    def run(lista):
        dicionario[lista[0]] = lista[1]
    return run

if __name__ == '__main__':
    coleta = 1

    tempo_presente = 80
    tempo_ativo = 90

    cur_path = os.path.dirname(__file__)
    path_coleta = os.path.relpath('..\\Coletas\\coleta ' + str(coleta) + '.txt', cur_path)

    dicionario_segundos = {}
    dicionario = {}

    arquivo_coleta_real = open("..\\Coletas\\coleta {} real.txt".format(str(coleta)))
    dicionario_coleta_real = {}
    linhas = arquivo_coleta_real.readlines()
    arquivo_coleta_real.close()

    linas_splitadas = list(map(lambda x: x.split(),linhas))
    list(map(add_dicionario_coleta_real(dicionario_coleta_real),linas_splitadas))

    ultimo_valor = linas_splitadas[0][1]

    arquivo_coleta = open("..\\Coletas\\coleta {}.txt".format(str(coleta)))
    # arquivo = open(path_coleta)
    linhas = arquivo_coleta.readlines()
    arquivo_coleta.close()

    primeira_linha = linhas[0].split()
    ultima_linha = linhas[-1].split()

    timestamp_inicial = int(primeira_linha[2])
    timestamp_atual = timestamp_inicial
    timestamp_final = int(ultima_linha[2])

    list(map(add_linha_dicionario, linhas))

    criar_cabecalho(coleta,tempo_presente,tempo_ativo)

    while timestamp_atual <= timestamp_final:
        texto_hora = get_texto_hora(timestamp_atual)
        if (texto_hora in dicionario_coleta_real):
            ultimo_valor = dicionario_coleta_real[texto_hora]

        worker(timestamp_atual,dicionario)
        contador = vigia_dicionario(timestamp_atual,dicionario,tempo_ativo,tempo_presente)

        segundo = timestamp_atual - timestamp_inicial
        salvar_em_arquivo(contador,coleta,tempo_presente,tempo_ativo,segundo,timestamp_atual,texto_hora, ultimo_valor)
        print(str(segundo + 1) + "," + str(contador))
        timestamp_atual += 1
