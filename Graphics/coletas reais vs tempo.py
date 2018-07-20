import numpy
from functools import reduce

import matplotlib.pyplot as plt
import pandas as pd

numero_coletas = 8
data_frames = []

for coleta in range(1, numero_coletas):
    arq = open("../Coletas/coleta {} real.txt".format(coleta), "r")
    tempo = arq.readlines()
    dado = []
    data = []
    for linha in tempo:
        linha = linha.split()
        data.append(linha[0])
        dado.append(linha[1])

    for x in range(len(data)):
        data[x] = float(data[x].replace(":", "."))

    print(dado)
    print(data)
    dic = {"coleta {}".format(coleta): dado, "hora": data}
    df = pd.DataFrame(dic)
    df = df.set_index("hora")
    data_frames.append(df)
    arq.close()

# print(data_frames)
result = reduce(lambda left, right: left.merge(right, how='outer', left_index=True, right_on="hora", left_on="hora"),
                data_frames)

plt.plot(result)
plt.legend([*result.keys()])
plt.xlabel("Hora")
plt.ylabel("Lotação")
plt.show()
