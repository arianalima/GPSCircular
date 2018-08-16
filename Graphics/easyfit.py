entrada = open("..\\IA\\df_coletas.arff")
texto = entrada.read()
entrada.close()
lista = texto.split("\n")
lista = lista[13:len(lista):10]
resultado = "\n".join(lista)
saida = open("easyfit.csv","w")
saida.write(resultado)
saida.close()


