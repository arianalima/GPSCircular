import pandas as pd
from ggplot import *

df1 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p80 a90.csv")
df2 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p80 a150.csv")
df3 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p80 a180.csv")
df4 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p60 a90.csv")
df5 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p60 a150.csv")
df6 = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p60 a180.csv")

print(df1["calculo"].map(str))

df1["calculo1_80_90"] = df1["calculo"].map(str)
df2["calculo1_80_150"] = df2["calculo"].map(str)
df3["calculo1_80_180"] = df3["calculo"].map(str)
df4["calculo1_60_90"] = df4["calculo"].map(str)
df5["calculo1_60_150"] = df5["calculo"].map(str)
df6["calculo1_60_180"] = df6["calculo"].map(str)

print(2)
g = ggplot(data=df) +\
    geom_line(aes(x="segundo", y="calculo"), data=df)
g.show()


# from ggplot import ggplot, geom_line, aes
# import pandas as pd
#
# df = pd.DataFrame({'x':range(15),'a': range(5,16), 'b': range(5, 16), 'c': range(7, 18)})
# a = ggplot(aes(x='x'), data=df) +\
#     geom_line(aes(y='a'), color='blue') +\
#     geom_line(aes(y='b'), color='red') +\
#     geom_line(aes(y='c'), color='green')
# a.show()