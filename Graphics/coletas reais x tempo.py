import numpy
from functools import reduce

import matplotlib.pyplot as plt
import pandas as pd

numero_coletas = 28
data_frames = []


def create_df(lista, coleta):
    try:
        arq = open("../Coletas/coleta {} real.txt".format(coleta), "r")
        tempo = arq.readlines()
        dado = []
        data = []

        def get_dados(linha):
            linha = linha.split()
            data.append(linha[0])
            dado.append(int(linha[1]))
        list(map(lambda x: get_dados(x), tempo))

        def reformat(indice):
            data[indice] = float(data[indice].replace(":", "."))

        list(map(lambda x: reformat(x), range(len(data))))

        dic = {"coleta {}".format(coleta): dado, "hora": data}
        df = pd.DataFrame(dic)
        df = df.set_index("hora")
        data_frames.append(df)
        arq.close()
    except:
        pass

list(map(lambda x : create_df(data_frames,x), range(1,numero_coletas)))
# print(data_frames)
result = reduce(lambda left, right: left.merge(right, how='outer', left_index=True, right_on="hora"),
                data_frames)
result = pd.DataFrame(result)
plt.plot(result, 'ro')
# plt.legend([*result.keys()])
plt.xlabel("Hora")
plt.ylabel("Lotação")
plt.show()
