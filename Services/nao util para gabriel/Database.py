import pymysql

def executa_SQL(pSQL, cursor, db):
    try:
        cursor.execute(pSQL)
        db.commit()
        return True
    except Exception as e:
        print(e)
        print("Error: Não foi possível executar o SQL")
        db.rollback()

def Busca_SQL(pSQL, cursor):
    try:
        cursor.execute(pSQL)
        results = cursor.fetchall()
        return results
    except:
        print("Error: Não foi possível buscar os dados")
        return False

def criarTabelas(cursor, db):

    tabelaPessoa = "CREATE TABLE IF NOT EXISTS PESSOA (ID INT NOT NULL AUTO_INCREMENT, MAC VARCHAR(17) NULL, SINAL INT NULL, TIMESTAMP INT NULL, PRIMARY KEY (ID) ) ENGINE=InnoDB"
    executa_SQL(tabelaPessoa, cursor, db)

    tabelaLocalizacao = "CREATE TABLE IF NOT EXISTS LOCALIZACAO (ID INT NOT NULL AUTO_INCREMENT, IDNODE INT NOT NULL, LATITUDE DOUBLE NULL, LONGITUDE DOUBLE NULL, TIMESTAMP INT NULL, PRIMARY KEY (ID) ) ENGINE=InnoDB"
    executa_SQL(tabelaLocalizacao, cursor, db)

    tabelaLotacao = "CREATE TABLE IF NOT EXISTS LOTACAO (ID INT NOT NULL AUTO_INCREMENT, LOTACAO INT NULL, TIMESTAMP INT NULL, PRIMARY KEY (ID) ) ENGINE=InnoDB"
    executa_SQL(tabelaLotacao, cursor, db)

def inicializarBanco(servidor='127.0.0.1', usuario='root',senha=''):
    try:
        db = pymysql.connect(servidor, usuario, senha, 'CircularUFRPE')
        cursor = db.cursor()
        return cursor, db
    except:
        db = pymysql.connect(servidor, usuario, senha, '')
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE CircularUFRPE DEFAULT CHARACTER SET utf8")

        db = pymysql.connect(servidor, usuario, senha, 'CircularUFRPE')
        cursor = db.cursor()
        criarTabelas(cursor, db)
        return cursor, db

global cursor, db
cursor, db = inicializarBanco()


def inserirPessoa(mac, sinal, timestamp):
    pSQL = "INSERT INTO circularufrpe.pessoa(MAC, SINAL, TIMESTAMP) VALUES ('%s', %s, %s ) "%(mac,str(sinal),str(timestamp))
    insercao = executa_SQL(pSQL, cursor, db)
    if insercao == True:
        return ("Pessoa inserida com sucesso!")
    else:
        return ("Não foi possível inserir a pessoa.")

def inserirLocalizacao(idNode, latitude, longitude, timestamp):
    pSQL = "INSERT INTO circularufrpe.localizacao (IDNODE, LATITUDE, LONGITUDE, TIMESTAMP) VALUES (%s, %s, %s, %s)"%(str(idNode), str(latitude), str(longitude), str(timestamp))
    insercao = executa_SQL(pSQL, cursor, db)
    if insercao == True:
        return ("Localização inserida com sucesso!")
    else:
        return ("Não foi possível inserir a localização.")

def inserirLotacao(lotacao,timestamp):
    pSQL = "INSERT INTO circularufrpe.lotacao (LOTACAO, TIMESTAMP) VALUES (%s, %s)" % (str(lotacao), str(timestamp))
    insercao = executa_SQL(pSQL, cursor, db)
    if insercao == True:
        return ("Lotação inserida com sucesso!")
    else:
        return ("Não foi possível inserir a lotação.")

def getLotacao():
    pSQL = "SELECT LOTACAO from circularufrpe.lotacao ORDER BY ID DESC LIMIT 1"
    resultado = Busca_SQL(pSQL, cursor)
    if len(resultado)==0:
        return ("-1")
    return str(resultado[0][0])


# inserirLotacao(30,1517843934)
# print(getLotacao())
# inserirPessoa("00:19:B9:FB:E2:58",-50,676867867)
# inserirLocalizacao(211, 99.99292, 12.0101, 3898022)
