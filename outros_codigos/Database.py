import pymysql

def executa_SQL(pSQL, cursor, db):
    try:
        cursor.execute(pSQL)
        db.commit()
        return True
    except:
        print("Error: Não foi possível executar o SQL")
        db.rollback()

def Busca_SQL(cursor, pSQL):
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

    tabelaCircular = "CREATE TABLE IF NOT EXISTS CIRCULAR (ID INT NOT NULL AUTO_INCREMENT, IDNODE INT NOT NULL, LOTACAO INT NULL, LATITUDE DOUBLE NULL, LONGITUDE DOUBLE NULL, TIMESTAMP INT NULL, PRIMARY KEY (ID) ) ENGINE=InnoDB"
    executa_SQL(tabelaCircular, cursor, db)

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

def inserirCircular(idNode, lotacao, latitude, longitude, timestamp):
    pSQL = "INSERT INTO circularufrpe.circular (IDNODE, LOTACAO, LATITUDE, LONGITUDE, TIMESTAMP) VALUES (%s, %s, %s, %s, %s)"%(str(idNode), str(lotacao), str(latitude), str(longitude), str(timestamp))
    insercao = executa_SQL(pSQL, cursor, db)
    if insercao == True:
        return ("Circular inserid com sucesso!")
    else:
        return ("Não foi possível inserir o circular.")

inserirPessoa("00:19:B9:FB:E2:58",-50,676867867)
inserirCircular(211,30,99.99292, 12.0101, 3898022)
