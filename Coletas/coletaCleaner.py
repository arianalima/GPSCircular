coleta = 9

f = open("coleta %s.txt"%coleta,"r")
a = f.read().split()
a = list(map(lambda x: x.replace("\n",""),a))
f.close()

f = open("coleta %d.txt"%coleta,"w")
list(map(lambda x : f.write(a[x]+" "+a[x+1]+" "+a[x+2]+"\n"),range(0,len(a),3)))
f.close()