import matplotlib.pyplot as plt
import pandas as pd

quantidadeColetas = 9
coleta = []
tempoPresente = 80
tempoAtivo = 90

# minutos = []

def formatar(numero, lista):
    arquivo = open("..\\Coletas\\csv's\\coleta " + str(numero) + " algoritmo p" + str(tempoPresente) + \
                   " a" + str(tempoAtivo) + ".csv")

    segundos = arquivo.readlines()
    for tempos in segundos[1:1700:]:
        tempos = tempos.split(",")
        # minutos.append(tempos[0])
        lista.append(tempos[1])


    arquivo.close()


def plot_resultado_minuto(lista):
    plt.figure()
    plt.plot(lista)
    plt.title("Coletas")
    plt.ylabel("lotação")
    plt.xlabel("tempo(s)")
    plt.tight_layout()
    plt.grid(alpha=0.8)
    plt.legend([*df.keys()])
    plt.show()


dic = {}
for x in range(1, quantidadeColetas):
    coleta = []
    formatar(x, coleta)
    n_coleta = coleta[1::]
    for i in range(len(n_coleta) - 1):
        n_coleta[i] = int(n_coleta[i])
    tamanho = len(n_coleta)
    if tamanho < 1700:
        for z in range(1700 - tamanho):
            n_coleta.append(0)
    dic["coleta "+str(x)] = n_coleta

df = pd.DataFrame(dic)
plot_resultado_minuto(df)
