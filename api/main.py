from flask import Flask, render_template, redirect, url_for, request, session
from auth import auth
from DAO import cnx, get_event_id, insert_anuncio, insertBLOB, insert_evento_e_categoria
import requests

app = Flask(__name__)
app.register_blueprint(auth)

app.secret_key = "uhrq3ur23guyrh"


def get_address_info(cep):
    url = f"https://api.brasilaberto.com/v1/zipcode/{cep}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data["result"]["city"]
        state = data["result"]["stateShortname"]
        return city, state
    else:
        return None, None


@app.route("/")
def default():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home_page.html")


@app.route("/editar_perfil")
def editar_perfil():
    if "loggedin" in session and session["loggedin"] is True:
        return render_template("dadosPessoal.html")
    else:
        return render_template(url_for("auth.login"))


@app.route("/criar_anuncio")
def criar_anuncio():
    if "loggedin" in session and session["loggedin"] is True:
        return render_template("anunciar.html")
    else:
        return render_template(url_for("auth.login"))


@app.route("/criar_anuncio", methods=["POST", "GET"])
def criar_anuncio_POST():
    if request.method == "POST":
        email = session["email"]
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        tipos = request.form.getlist("tipos")
        imagens = request.files.getlist("imagem")
        local = request.form.get("localizaçaocepext")
        cep = request.form.get("localizaçaocep")
        email_contato = request.form.get("email")
        telefone = request.form.get("telefone")
        instagram = request.form.get("Instagran")
        espaco_bool = request.form.get("espaço")
        tamanho = request.form.get("Tamanho")
        valor_diaria = request.form.get("valordiaria")

        cidade, estado = get_address_info(cep)

        print("Email:", email)
        print("Título:", titulo)
        print("Descrição:", descricao)
        print("Tipos de eventos:", tipos)
        print("Local:", local)
        print("cidade:", cidade)
        print("estado:", estado)
        print("CEP:", cep)
        print("Email de contato:", email_contato)
        print("Telefone:", telefone)
        print("Instagram:", instagram)
        print("Tamanho:", tamanho)

        # primeira operação de inserção
        insert_anuncio(
            email,
            estado,
            cidade,
            local,
            titulo,
            1,
            valor_diaria,
            tamanho,
            email_contato,
            telefone,
            instagram,
            descricao,
        )
        # pegar id do evento para fazer inserção em eventos_categorias e imagens
        id_anuncio = get_event_id(email, estado, cidade, local, titulo, tamanho)
        # fazer a inserção de cada imagem
        for imagem in imagens:
            if imagem.filename != "":
                print("condicional de filename ok")
                image_data = imagem.read()
                image_description = "Descrição da imagem"
                insertBLOB(id_anuncio, image_data, image_description)
        # fazer a inserção em tb_evento_e_categoria
        for tipo in tipos:
            insert_evento_e_categoria(id_anuncio, tipo)

        return redirect(url_for("home"))

    return render_template("anunciar.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port="3030")
