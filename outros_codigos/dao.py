import pymongo
import time

HOST = "127.0.0.1"
PORTA = 27017
BANCO = "circular_ufrpe"
COLECAO_POSICAO = "posicao_circular"
COLECAO_LOTACAO = "lotacao_circular"

cliente = pymongo.MongoClient(HOST, PORTA)

db = cliente[BANCO]

posicao = db[COLECAO_POSICAO]
lotacao = db[COLECAO_LOTACAO]


def add_posicao(obj_json):
    posicao.insert_one(obj_json)

def get_ultima_posicao():
    resultado = posicao[COLECAO_POSICAO].find().sort("date", pymongo.DESCENDING)
    #TODO: Comparar hora com a atual e ver se faz muito tempo
    print(resultado.count())

def add_lotacao(obj_json):
    lotacao.insert_one(obj_json)

def get_ultima_lotacao():
    resultado = lotacao[COLECAO_LOTACAO].find().sort("date", pymongo.DESCENDING)
    #TODO: Comparar hora com a atual e ver se faz muito tempo
    print(resultado.count())
