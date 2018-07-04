import os

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
    arquivo = open("..\\Coletas\\coleta "+ str(coleta) +" algoritmo p" + str(presente) + \
              " a" + str(ativo) + ".csv", "a")
    arquivo.write("segundo,calculo,timestamp" + "\n")
    arquivo.close()


def salvar_em_arquivo(contagem, coleta, presente, ativo, segundo, timestamp):
    arquivo = open("..\\Coletas\\coleta "+ str(coleta) +" algoritmo p" + str(presente) + \
              " a" + str(ativo) + ".csv", "a")
    arquivo.write("{},{},{}".format(str(segundo),str(contagem),str(timestamp)) + "\n")
    arquivo.close()

if __name__ == '__main__':
    coleta = 1

    tempo_presente = 80
    tempo_ativo = 90

    cur_path = os.path.dirname(__file__)
    path_coleta = os.path.relpath('..\\Coletas\\coleta' + str(coleta) + '.txt', cur_path)

    dicionario_segundos = {}
    dicionario = {}

    arquivo = open("..\\Coletas\\coleta" + str(coleta) + ".txt")
    # arquivo = open(path_coleta)
    linhas = arquivo.readlines()
    arquivo.close()

    primeira_linha = linhas[0].split()
    ultima_linha = linhas[-1].split()

    timestamp_inicial = int(primeira_linha[2])
    timestamp_atual = timestamp_inicial
    timestamp_final = int(ultima_linha[2])

    list(map(add_linha_dicionario, linhas))

    criar_cabecalho(coleta,tempo_presente,tempo_ativo)

    while timestamp_atual <= timestamp_final:
        worker(timestamp_atual,dicionario)
        contador = vigia_dicionario(timestamp_atual,dicionario,tempo_ativo,tempo_presente)

        segundo = timestamp_atual - timestamp_inicial


        salvar_em_arquivo(contador,coleta,tempo_presente,tempo_ativo,segundo,timestamp_atual)
        print(str(segundo + 1) + "," + str(contador))
        timestamp_atual += 1