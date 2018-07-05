from ggplot import *
import pandas as pd

quantidadeColetas = 9

tempoPresente = 80
tempoAtivo = 90

minutos = []

def list_minutos(coleta):
    arquivo = open("..\\Coletas\\coleta " + str(coleta) + " algoritmo p" + str(tempoPresente) + \
                   " a" + str(tempoAtivo) + ".csv")

    segundos = arquivo.read().split()[-1]\
                    .split(",")[0]

    arquivo.close()
    minuto = int(segundos) // 60
    minutos.append(minuto)

list(map(lambda x : list_minutos(x),range(1,quantidadeColetas+1)))

# print(minutos)
def gg_plota_bar():
   df = pd.DataFrame({'Minutos': minutos,'Coletas':list(range(quantidadeColetas))})
   plt = ggplot(aes(x='Minutos',y='Coletas'), data=df) + geom_bar(fill= 'blue') +ggtitle("Tempo médio das viagens")
   plt.show()

gg_plota_bar()

