import pandas as pd

primeira_coleta = 1
p = 80
a = 90
ultima_coleta = 9

range_coletas = range(primeira_coleta,ultima_coleta+1)

def coleta_dtframe(coleta):
    global p
    global a
    csv_name = "coleta {} algoritmo p{} a{}.csv".format(coleta,p,a)
    dtframe = pd.read_csv("..\\Coletas\\" + csv_name)
    dtframe_return = pd.DataFrame({})
    dtframe_return["calculo"] = dtframe["calculo"].map(int)
    return dtframe_return

dt_frames = list(map(coleta_dtframe,range_coletas))
newdf = pd.concat(dt_frames)
newdf.to_csv("..\\Coletas\\" + "easyfit p{} a{}.csv".format(p,a))