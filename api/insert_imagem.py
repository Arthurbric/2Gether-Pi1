import mysql.connector

# Conectar ao banco de dados MySQL
cnx = mysql.connector.connect(
    user="root",
    password="Gatitcha1",
    host="127.0.0.1",
    database="db_eventos",
)


cursor = cnx.cursor()

# Caminho para o arquivo de imagem
image_path = r'C:\Users\Guilherme Henrique\Pictures\fotos pinterest\imagen.jpg'

# Ler o arquivo de imagem em formato binário
with open(image_path, 'rb') as file:
    binary_data = file.read()

# SQL para inserir a imagem na tabela tb_imagem_evento
insert_query = '''
INSERT INTO tb_imagem_evento (image_event_id, event_images, image_description)
VALUES (%s, %s, %s)
'''

# Dados a serem inseridos
data = (2, binary_data, 'Descrição da Imagem')

# Executar o comando de inserção
cursor.execute(insert_query, data)

# Confirmar a transação
cnx.commit()

# Fechar o cursor e a conexão
cursor.close()
cnx.close()

print("Imagem inserida com sucesso!")
