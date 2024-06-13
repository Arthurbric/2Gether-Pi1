import mysql.connector


# try:
#     cnx = mysql.connector.connect(
#         user="root",
#         password="senhaUltraSegura",
#         host="192.168.0.102",
#         database="db_eventos",
#     )
# except:
#     cnx = mysql.connector.connect(
#         user="root",
#         password="Gatitcha1",
#         host="127.0.0.1",
#         database="db_eventos",
#     )
#     try:
#         cnx = mysql.connector.connect(
#         user="root",
#         password="passywassy",
#         host="127.0.0.1",
#         database="db_eventos",
#         )

#     except:
#         print("nenhuma conexão encontrada")

cnx = mysql.connector.connect(
    user="root",
    password="passywassy",
    host="127.0.0.1",
    database="db_eventos",
)

print(cnx.is_connected())


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


def insertCadastro(email, senha, nome1, nome2, cpf, userType):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO tb_usuario (user_name, user_email, user_password, user_cpf, user_type) VALUES ('"
        + nome1
        + " "
        + nome2
        + "', '"
        + email
        + "', '"
        + senha
        + "', '"
        + cpf
        + "', '"
        + userType
        +"')"
    )
    cursor.execute(query)
    cnx.commit()
    cursor.close()


def updateCadastro(id, nome, email, telefone):
    cursor = cnx.cursor()
    query = "UPDATE tb_usuario SET user_name = %s, user_email = %s, user_phone = %s WHERE user_id = %s"
    cursor.execute(query, [nome, email, telefone, id])
    cnx.commit()
    cursor.close()


def updateSenha(id, senha):
    cursor = cnx.cursor()
    query = "UPDATE tb_usuario SET user_password = %s WHERE user_id = %s"
    cursor.execute(query, [senha, id])
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


def update_senha(email, senha):
    cursor = cnx.cursor()

    query = (
        f"UPDATE tb_usuario set user_password = '{senha}' where user_email = '{email}'"
    )

    cursor.execute(query)
    cnx.commit()
    cursor.close()


def insert_municipio(estado, cidade):
    cursor = cnx.cursor()

    query = "INSERT INTO tb_local (address_state, address_city) VALUES (%s, %s)"

    cursor.execute(query, [estado, cidade])
    cnx.commit()
    cursor.close()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        binaryData = file.read()
    return binaryData


# caso valor nulo adicionar valor padrão?
def insert_anuncio(
    user_email,
    estado,
    cidade,
    location_address,
    event_name,
    event_add_status,
    event_space,
    event_daily_price,
    event_size,
    event_email,
    event_telefone,
    event_instagram,
    event_description
):

    cursor = cnx.cursor()

    query = """INSERT INTO tb_eventos (owner_event, location_event, location_address, event_name, event_description,
            event_instagram, event_add_status, event_space, event_daily_price, event_size, event_email, event_telefone)
             VALUES ((SELECT user_id FROM tb_usuario WHERE user_email = %s), (SELECT address_id FROM tb_local WHERE address_state = %s AND address_city = %s), 
             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(
        query,
        [
            user_email,
            estado,
            cidade,
            location_address,
            event_name,
            event_description,
            event_instagram,
            event_add_status,
            event_space,
            event_daily_price,
            event_size,
            event_email,
            event_telefone
        ]
    )
    cnx.commit()


def insert_evento_e_categoria(event_id, event_category):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO tb_evento_e_categoria (event_id, event_category)"
        "VALUES (%s, (SELECT category_id FROM tb_categoria WHERE tipo_categoria = %s))"
    )
    cursor.execute(query, [event_id, event_category])
    cnx.commit()


def get_event_id(user_email, estado, cidade, location_address, event_name, event_size):
    cursor = cnx.cursor()

    query = """SELECT event_id FROM tb_eventos WHERE (SELECT user_id FROM tb_usuario WHERE user_email = %s) AND 
             (SELECT address_id FROM tb_local WHERE address_state = %s AND address_city = %s) 
             AND location_address = %s AND event_name = %s AND event_size = %s LIMIT 0, 1"""
    cursor.execute(
        query, [user_email, estado, cidade, location_address, event_name, event_size]
    )

    # querySet = cursor.fetchone()

    # result = querySet[0]

    # cursor.close()

    # return result

    querySet = cursor.fetchone()

    if querySet == None:
        print("im die")

    else:
        result = querySet[0]

        # print(result)

        cursor.close()

        return result


def insertBLOB(image_event_id, event_image, image_description):
    print("função insertBLOB iniciada")
    cursor = cnx.cursor()
    sql_insert_blob_query = """ INSERT INTO tb_imagem_evento
                          (image_event_id, event_images, image_description) VALUES (%s,%s,%s)"""

    # Convert data into tuple format
    insert_blob_tuple = (image_event_id, event_image, image_description)
    cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    cnx.commit()
    cursor.close()
