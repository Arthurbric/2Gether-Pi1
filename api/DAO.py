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
    password="senha123",
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

def deleteEvent(event_id):
    cursor = cnx.cursor()

    query = """ DELETE FROM tb_eventos WHERE event_id = %s """

    cursor.execute(query, [event_id])
    cnx.commit
    cursor.close()

def getMunicipioId(cidade, uf):
    cursor = cnx.cursor()
    
    query = """ SELECT address_id FROM tb_local WHERE address_city="%s" AND address_state="%s" """

    cursor.execute(query, [cidade, uf])

    querySet = cursor.fetchone()

    if querySet == None:
        return querySet

    else:
        result = querySet[0]

        # print(result)

        cursor.close()

        return result

def updateEvent(event_id, local, endereco, nome, descricao, instagram, status, espaco, diaria, tamanho, email, telefone):
    cursor = cnx.cursor()
    
    query = """ UPDATE tb_eventos SET location_event = %s, location_address = "%s", event_name = "%s", event_description = "%s",
                event_instagram = "%s", event_add_status = %s, event_space = %s, event_daily_price = "%s", event_size = "%s", 
                event_email = "%s", event_telefone="%s" WHERE event_id = %s """
    
    cursor.execute(query, [local,
                           endereco,
                           nome,
                           descricao,
                           instagram,
                           status,
                           espaco,
                           diaria,
                           tamanho,
                           email,
                           telefone,
                           event_id
                           ])
    cnx.commit()
    cursor.close()

def counterListEventsUser(User_id):
    id = User_id

    query = (
        "SELECT COUNT(*) FROM tb_eventos WHERE owner_event = %s"
    )

    cursor = cnx.cursor()
    cursor.execute(query, [id])

    querySet = cursor.fetchone()

    count = querySet[0]

    cursor.close()

    return count


def listEventsUserEdit(User_id):
    id = User_id
    i = 1
    sHtml = ""

    cursor = cnx.cursor()
    query = f"SELECT * FROM tb_eventos WHERE owner_event = %s"

    try:
        cursor.execute(query, [id])
        rows = cursor.fetchall()

        if not rows:
            return "<p>Esse usuário não possui anuncios ativos!</p>"


        for row in rows:

            owner_event = str(row[1])

            event_id= str(row[0])
            event_name= row[4]
            event_description= row[5]
            event_instagram= row[6]
            event_email= row[11]
            event_telefone= str(row[12])
            event_daily_price= str(row[9])
            event_size= str(row[10])
            location_address= row[3]

            i = str(i)


            imagem = "placeholder"

            sHtml =sHtml                   + """<div class="card">
                                                    <div class="card-header" id="heading""" + i + """">
                                                        <h5 class="mb-0">
                                                            <button class="btn btn-link" type="button"
                                                                data-toggle="collapse" data-target="#collapse""" + i + """"
                                                                aria-expanded="true" aria-controls="collapse""" + i + """">
                                                                """ + event_name + """
                                                            </button>
                                                        </h5>
                                                    </div>

                                                    <div id="collapse""" + i +  """" class="collapse show" aria-labelledby="heading""" + i + """"
                                                        data-parent="#accordionExample">
                                                        <form action="{{ url_for('salvar', idAnuncio = """ + event_id + """, acesso = 1) }}" method="post">    
                                                            <div class="card-body">

                                                            

                                                                <nav>




                                                                    <div class="card-body media align-items-center">
                                                                        <img src=" """ + imagem + """ "
                                                                            style="border-radius: 5%; margin-bottom: 20px; height: 300px;"
                                                                            alt="" id="imgAnuncio">
                                                                        <div class="media-body ml-4">
                                                                            <label class="btn btn-outline-primary">
                                                                                Carregar Nova Foto
                                                                                <input type="file"
                                                                                    class="account-settings-fileinput"
                                                                                    onchange="previewImage(event)">
                                                                            </label> &nbsp;
                                                                            <button type="button"
                                                                                class="btn btn-default md-btn-flat"
                                                                                onclick="removeImage()">Apagar</button>
                                                                            <div class="text-light small mt-1">JPG, GIF ou PNG
                                                                                permitidos. Tamanho máximo de
                                                                                1600K</div>
                                                                        </div>
                                                                    </div>





                                                                    <div class="form-group">
                                                                        <label class="form-label">Nome do anúncio</label>
                                                                        <input name="nome" type="text" class="form-control" value=" """ + event_name + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Descrição do anúncio</label>
                                                                        <textarea name="descricao" class="form-control"
                                                                            rows="5">""" + event_description + """</textarea>
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Instagram</label>
                                                                        <input name="instagram" type="text" class="form-control" value=" """ + event_instagram + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Email</label>
                                                                        <input name="email" type="text" class="form-control" value=" """ + event_email + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Telefone p/ contato</label>
                                                                        <input name="telefone" type="text" class="form-control" value=" """ + event_telefone + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Valor da Diária</label>
                                                                        <input name="diaria" type="text" class="form-control" value=" """ + event_daily_price + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Lotação máxima</label>
                                                                        <input name="tamanho" type="number" class="form-control" value=" """ + event_size + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label">Endereço</label>
                                                                        <input name = "endereco" type="text" class="form-control"
                                                                            value=" """ + location_address + """ ">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <label class="form-label" for="cepInput""" + i +"""">CEP</label>
                                                                        <input type="text" id="cepInput""" + i +"""" class="form-control"
                                                                            placeholder="Digite o CEP: 99999-999"
                                                                            oninput="buscarCEP""" + i +"""()"><br>

                                                                        <div id="resultado" style="display: none;">

                                                                            <div>
                                                                                <label
                                                                                    for="logradouroExibido">Logradouro</label>
                                                                                <input type="text" name="logradouroExibido" id="logradouroExibido"
                                                                                    class="form-control" readonly><br>
                                                                            </div>
                                                                            <div>
                                                                                <label for="bairroExibido">Bairro</label>
                                                                                <input type="text" name="bairroExibido" id="bairroExibido"
                                                                                    class="form-control" readonly><br>
                                                                            </div>
                                                                            <div>
                                                                                <label
                                                                                    for="localidadeExibido">Localidade</label>
                                                                                <input type="text" name="localidadeExibido" id="localidadeExibido"
                                                                                    class="form-control" readonly><br>
                                                                            </div>
                                                                            <div>
                                                                                <label for="ufExibido">UF</label>
                                                                                <input type="text" name="ufExibido" id="ufExibido"
                                                                                    class="form-control" readonly><br>
                                                                            </div>

                                                                            <script>
                                                                                async function buscarCEP""" + i +"""() {
                                                                                    const cep = document.getElementById('cepInput""" + i +"""').value;
                                                                                    // Only proceed if the input length matches the expected CEP format
                                                                                    if (cep.length === 8) {
                                                                                        const url = `https://viacep.com.br/ws/${cep}/json/`;

                                                                                        try {
                                                                                            const response = await fetch(url);
                                                                                            const data = await response.json();

                                                                                            if (data.erro) {
                                                                                                alert('CEP não encontrado!');
                                                                                                return;
                                                                                            }

                                                                                            document.getElementById('resultado').style.display = 'block';
                                                                                            // document.getElementById('cepExibido').value = data.cep;
                                                                                            document.getElementById('logradouroExibido').value = data.logradouro;
                                                                                            document.getElementById('bairroExibido').value = data.bairro;
                                                                                            document.getElementById('localidadeExibido').value = data.localidade;
                                                                                            document.getElementById('ufExibido').value = data.uf;
                                                                                        } catch (error) {
                                                                                            console.error(error);
                                                                                            alert('Erro ao buscar CEP!');
                                                                                        }
                                                                                    }
                                                                                }


                                                                            </script>

                                                                            <br>
                                                                            <form id="deletar""" + i + """" action="{{ url_for('deletar', idAnuncio = """ + event_id + """, acesso = 1) }}" method="post" style="display:none">
                                                                            </form>
                                                                            <h5 class="mb-2">
                                                                                <a href="#"
                                                                                    class="float-right text-muted text-tiny"
                                                                                    id="apagar-anuncio" onclick="document.getElementById("deletar""" + i + """").submit();">
                                                                                    <i class="ion ion-md-close"></i> Apagar
                                                                                </a>
                                                                                <i class="ion ion-logo-google text-google"></i>
                                                                                Apagar Anúncio:
                                                                            </h5>

                                                                        </div>



                                                                </nav>


                                                            </div>
                                                            <div class="text-right mt-3" style="margin: 0 20px 15px 0; ">
                                                                <input type="submit" class="btn btn-primary" value="Salvar Alterações">&nbsp;
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>"""
            
            i = int(i)
            
            i += 1

    except Exception as e:
        return f"<p>Um erro ocorreu: {e}</p>"
    
    return sHtml 
