import mysql.connector


#print(cnx.is_connected())

cnx = mysql.connector.connect(
        user="root", password="senhaUltraSegura", host="192.168.0.103", database="db_eventos"
)
def CheckLogin(user, senha):
    query = ('SELECT COUNT(*) FROM tb_usuario WHERE user_email =  %s  AND user_password = %s')

    cursor = cnx.cursor()
    cursor.execute(query,[user, senha])

    querySet = cursor.fetchone()

    count = querySet[0]

    if count:
        print(cursor)
    else:
        print("n existe")

    cursor.close()

    return count

def CheckCadastro(coluna, atributo):
    query = f"SELECT COUNT(*) FROM tb_usuario WHERE {coluna} = %s"
    cursor = cnx.cursor()
    cursor.execute(query, [atributo])

    querySet = cursor.fetchone()

    count = querySet[0]

    if count:
        print(cursor)
    else:
        print("n existe")

    cursor.close()

    return count

def selectFromWhere(tabela, campoReferencia, valorReferencia, campoBuscado="*"):
    cursor = cnx.cursor()
    query = (f"SELECT {campoBuscado} FROM {tabela} WHERE {campoReferencia} = '{valorReferencia}'")

    cursor.execute(query)

    querySet = cursor.fetchone()

    result = querySet[0]

    cursor.close()

    return result

def insertCadastro(email, senha, nome1, nome2, cpf):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf) VALUES ('"
        + nome1 
        + " "
        + nome2 
        + "', '"
        + email
        + "', '"
        + senha
        + "', '"
        + cpf
        + "')"
    )
    cursor.execute(query)
    cnx.commit()
    cursor.close()

def insertCodigo(email, verification_code, expiration_time):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO tb_verificacao_senha (user_id, user_email, verification_code, expiration_time) VALUES ("
        "(SELECT user_id FROM tb_usuario WHERE user_email = %s), %s, %s,NOW() + INTERVAL %s MINUTE)"
    )
    cursor.execute(query, (email, email, verification_code, expiration_time))
    cnx.commit()
    cursor.close()