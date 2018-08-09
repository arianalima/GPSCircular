import pandas as pd
import datetime
import pytz

primeira_coleta = 1
p = 80
a = 90
ultima_coleta = 24

range_coletas = range(primeira_coleta,ultima_coleta + 1)

def get_menor_time_stamp(p,a):
    def get_menor(coleta):
        csv_name = "coleta {} algoritmo p{} a{}.csv".format(coleta, p, a)
        arquivo = open("..\\Coletas\\csv's\\" + csv_name)
        linhas = arquivo.readlines()
        linha_timestamp = linhas[1].split(",")
        menor_ts = linha_timestamp[2]
        segundos_extraidos = extract_segundos_dia(int(menor_ts))
        return segundos_extraidos
    return get_menor

def coleta_to_dtframe(p, a, menor_tempo):
    def subtrair_tempo_inicial(x, tempo_inicial):
        x = extract_segundos_dia(int(x))
        return x - int(tempo_inicial)

    def get_dt(coleta):
        csv_name = "coleta {} algoritmo p{} a{}.csv".format(coleta,p,a)
        dtframe = pd.read_csv("..\\Coletas\\csv's\\" + csv_name)
        dtframe_return = pd.DataFrame({})
        dtframe_return["timestamp"] = dtframe["timestamp"].apply(subtrair_tempo_inicial,args=(menor_tempo,))
        dtframe_return["calculo"] = dtframe["calculo"].map(int)
        return dtframe_return
    return get_dt

def extract_segundos_dia(timestamp):
    data = datetime.datetime.fromtimestamp(timestamp, pytz.UTC)
    hora = data.hour
    minuto = data.minute
    segundo = data.second
    qtd_segundos = (hora * 3600)+ (minuto *60) + segundo
    return qtd_segundos

tempos = list(map(get_menor_time_stamp(p,a),range_coletas))
menor_tempo = sorted(tempos)[0]
segundos_menos_tempo = extract_segundos_dia(menor_tempo)
dt_frames = list(map(coleta_to_dtframe(p,a,segundos_menos_tempo),range_coletas))
newdf = pd.concat(dt_frames)
newdf.to_csv("..\\Coletas\\" + "easyfit p{} a{}.csv".format(p,a))
