import pandas as pd
from ggplot import *

df1 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p80 a90.csv")
df2 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p80 a150.csv")
df3 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p80 a180.csv")
df4 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p60 a90.csv")
df5 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p60 a150.csv")
df6 = pd.read_csv("..\\Coletas\\csv's\\coleta 1 algoritmo p60 a180.csv")

newdf = pd.DataFrame({})

newdf["segundo"] = df1["segundo"].map(str)
newdf["valor_real"] = df1["valor_real"].map(str)
newdf["calculo1_80_90"] = df1["calculo"].map(str)
newdf["calculo1_80_150"] = df2["calculo"].map(str)
newdf["calculo1_80_180"] = df3["calculo"].map(str)
newdf["calculo1_60_90"] = df4["calculo"].map(str)
newdf["calculo1_60_150"] = df5["calculo"].map(str)
newdf["calculo1_60_180"] = df6["calculo"].map(str)

newdf.to_csv("coleta1_completa.csv")

newdf["x"] = newdf.index
g = ggplot(aes(x='segundo'), data=newdf) +\
    geom_line(aes(y='valor_real'), color='blue')
    # geom_line(aes(y='calculo1_80_90'), color='red') +\
    # geom_line(aes(y='calculo1_80_150'), color='green')
g.show()

