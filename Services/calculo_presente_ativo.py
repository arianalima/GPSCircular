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

    segundo = timestamp - timestamp_inicial

    def salvar_em_arquivo(contagem):
        arquivo = open("tesedicionario" + str(tempo_vida_ativo) + ".txt","a")
        arquivo.write(str(contagem) + "\n")
        arquivo.close()

    salvar_em_arquivo(contador)
    print(str(segundo + 1) + "," + str(contador))


if __name__ == '__main__':
    dicionario_segundos = {}
    dicionario_150 = {}

    timestamp_inicial = 1516185697
    timestamp_atual = 1516185697

    arquivo = open("coleta1.txt")
    linhas = arquivo.readlines()
    arquivo.close()
    list(map(add_linha_dicionario, linhas))

    while True:
        worker(timestamp_atual,dicionario_150)
        vigia_dicionario(timestamp_atual,dicionario_150,90,tempo_vida_presente=80)
        timestamp_atual += 1