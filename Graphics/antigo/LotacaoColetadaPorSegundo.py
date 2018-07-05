import matplotlib.pyplot as plt
f = open('coleta 1.txt','r')
data = f.readlines()
for line in range(len(data)):
    data[line] = data[line].split()
f.close()

""" plot_list: list(segundo*len(macs)) """
macs, plot_list = [], []
timestamp_inicial = int(data[0][2])
global segundo

for line in range(len(data)):
    timestamp = data[line][2]
    segundo = int(timestamp) - timestamp_inicial + 1
    try:
        next_timestamp = data[line+1][2]
    except IndexError:
        next_timestamp = -1
    mac = data[line][0]
    if mac not in macs:
        macs.append(mac)
        plot_list.append(segundo)
    if timestamp!=next_timestamp:
        # mac_time.append((segundo, len(macs)))
        macs=[]

print(plot_list)
plt.hist(plot_list, bins=segundo, alpha=0.8, histtype='step', ec='black', fill=False)
plt.grid(linestyle='dashdot')
plt.xlabel('segundos')
plt.ylabel('lotaçao')
plt.title("Lotação Coletada")
plt.show()