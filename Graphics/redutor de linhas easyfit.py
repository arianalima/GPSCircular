from operator import itemgetter
p = 80
a = 90
csv_name = "easyfit p{} a{}.csv".format(p,a)
arquivo = open("..\\Coletas\\" + csv_name)
texto = arquivo.readlines()
arquivo.close()
tamanho = len(texto)
indexes = range(0,tamanho,9)
lista_reduzida = itemgetter(*indexes)(texto)
arquivo = open("..\\Coletas\\" + csv_name,"w")
arquivo.writelines(lista_reduzida)