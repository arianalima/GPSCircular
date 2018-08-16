from itertools import product
P = [60,80]
A = [90,150,180]

def get_coletas(p_a):
    p, a = p_a
    x = open("..\\IA\\df_coletas_p{}a{}.arff".format(p,a)).read()
    lista = x.split("\n")
    return lista[13:len(lista)]

def getClassification(lotacao_real):
    if lotacao_real > 43:
        return "superlotado"
    elif 43 >= lotacao_real >= 33:
        return "lotado"
    elif 33 > lotacao_real >= 23:
        return "normal"
    else:
        return "vazio"

def count_measeruments(coleta):
    total = len(coleta)
    corretos = len(list(filter(lambda x: x[0] == x[1],coleta)))
    porcentagem_corretos = round(((corretos*100)/total),2)
    vazio = len(list(filter(lambda x: x[0]=='vazio',coleta)))
    normal = len(list(filter(lambda x: x[0] == 'normal', coleta)))
    lotado = len(list(filter(lambda x: x[0] == 'lotado', coleta)))
    superlotado = len(list(filter(lambda x: x[0] == 'superlotado', coleta)))
    return [corretos,porcentagem_corretos,vazio,normal,lotado,superlotado]

def measure(coleta):
    lista = list(map(lambda x:x.split(","),coleta))
    lista_linhas = list(filter(lambda x: x != [""],lista))
    tuplas_linhas = list(map(lambda x: [getClassification(int(x[2])),x[-1]],lista_linhas))
    result = count_measeruments(tuplas_linhas)
    return result

if __name__ == "__main__":
    inputs = list(product(P, A))
    coletas = list(map(get_coletas, inputs))
    resultado_coletas = list(map(measure,coletas))

    print(1)