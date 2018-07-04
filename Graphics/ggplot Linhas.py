import pandas as pd
from ggplot import *

df = pd.read_csv("..\\Coletas\\coleta 1 algoritmo p80 a90.csv")

g = ggplot(aes(x="segundo", y="calculo"), data=df) +\
    geom_line()
g.show()