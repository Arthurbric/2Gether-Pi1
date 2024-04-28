import mysql.connector


# print(cnx.is_connected())
try:
    cnx = mysql.connector.connect(
        user="root",
        password="senhaUltraSegura",
        host="192.168.0.102",
        database="db_eventos",
    )
except:
    cnx = mysql.connector.connect(
        user="root",
        password="Gatitcha1",
        host="127.0.0.1",
        database="db_eventos",
    )

def CheckLogin(user, senha):
    query = (
        "SELECT COUNT(*) FROM tb_usuario WHERE user_email =  %s  AND user_password = %s"
    )

    cursor = cnx.cursor()
    cursor.execute(query, [user, senha])

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
    query = f"SELECT {campoBuscado} FROM {tabela} WHERE {campoReferencia} = '{valorReferencia}'"

    cursor.execute(query)

    querySet = cursor.fetchone()

    if querySet == None:
        return querySet
    
    else:
        result = querySet[0]

        # print(result)

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


def insertCodigo(email, verification_code, time):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO tb_verificacao_senha (user_id, user_email, verification_code, expiration_time) VALUES ("
        "(SELECT user_id FROM tb_usuario WHERE user_email = %s), %s, %s, %s)"
    )
    cursor.execute(query, [email, email, verification_code, time])
    cnx.commit()
    cursor.close()


def deleteCodigo(email):
    cursor = cnx.cursor()

    query = "DELETE FROM tb_verificacao_senha WHERE user_email = '" + email + "'"

    cursor.execute(query)
    cnx.commit()
    cursor.close()
