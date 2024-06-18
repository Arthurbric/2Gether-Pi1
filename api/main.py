from flask import Flask, render_template, redirect, url_for, request, session, flash
from auth import auth
from DAO import *
import requests
import re
from hashlib import sha256

app = Flask(__name__)
app.register_blueprint(auth)

app.secret_key = "uhrq3ur23guyrh"


def get_address_info(cep):
    url = f"https://api.brasilaberto.com/v1/zipcode/{cep}"
    response = requests.get(url)
    print(response)
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
        id = session["id"]
        nome = session["nome"]
        email = session["email"]
        telefone = selectFromWhere(
            "tb_usuario", "user_id", session["id"], "user_phone"
        )
        cpf = selectFromWhere("tb_usuario", "user_id", session["id"], "user_cpf")
        sHtml = listEventsUserEdit(id)
        countEventos = counterListEventsUser(id)
        return render_template(
            "dadosPessoal.html", nome=nome, email=email, telefone=telefone, cpf=cpf, sHtml = sHtml, countEventos = countEventos
        )
    else:
        return render_template(url_for("auth.login"))


@app.route("/editar_perfil", methods=["POST"])
def editar_perfil_post():

    if "form1-submit" in request.form:
        id = session["id"]

        if "nome" in request.form and request.form["nome"] != "":
            nome = request.form.get("nome")
        else:
            nome = selectFromWhere("tb_usuario", "user_id", session["id"], "user_name")

        if "email" in request.form and request.form["email"] != "":
            email = request.form.get("email")
        else:
            email = selectFromWhere("tb_usuario", "user_id", session["id"], "user_email")

        if "telefone" in request.form and request.form["telefone"] != "":
            telefone = request.form.get("telefone")
        else:
            telefone = selectFromWhere("tb_usuario", "user_id", session["id"], "user_phone")

        if email == selectFromWhere("tb_usuario", "user_id", session["id"], "user_email"):
            checkEmail = 0
        
        else:
            checkEmail = CheckCadastro("user_email", email)

        if checkEmail >= 1:
            flash("Email já cadastrado!")
            return redirect(url_for("editar_perfil"))

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            updateCadastro(id, nome, email, telefone)
            session["nome"] = nome
            session["email"] = email

            flash("Atualizado com sucesso!")
            return redirect(url_for("editar_perfil"))
        else:
            flash("Email inválido!")
            return redirect(url_for("editar_perfil"))

    if "form2-submit" in request.form:
        id = session["id"]

        senhaAtual = request.form.get("senha-atual")

        novaSenha = request.form.get("senha-nova")
        novaSenhaConfirma = request.form.get("confirma-senha-nova")

        senhaHash = sha256(senhaAtual.encode("utf-8")).hexdigest()

        count = CheckLogin(session["email"], senhaHash)

        if count == 0:
            flash("Senha atual incorreta!")
            return redirect(url_for("editar_perfil"))

        else:
            if novaSenha != novaSenhaConfirma:
                flash("Confirmação de senha nova não correspondente!")
                return redirect(url_for("editar_perfil"))
            else:
                novaSenhaHash = sha256(novaSenha.encode("utf-8")).hexdigest()
                updateSenha(id, novaSenhaHash)

                flash("Atualizado com sucesso!")
                return redirect(url_for("editar_perfil"))
            

@app.route("/salvar", methods=["POST"])
def salvar():

    try:

        if int(request.args["acesso"]) == 1:

            idAnuncio = request.args.get("idAnuncio")

            nome = request.form.get("nome")
            endereco = request.form.get("endereco")
            logradouro = request.form.get("logradouroExibido")
            localidade = request.form.get("localidadeExibido")
            uf = request.form.get("ufExibido")
            descricao = request.form.get("descricao")
            instagram = request.form.get("instagram")
            status = 1
            space = 1
            preco = request.form.get("diaria")
            tamanhoLocal = request.form.get("tamanho")
            email = request.form.get("email")
            telefone = request.form.get("telefone")

            endCompleto = endereco + ", " + logradouro

            idMunicipio = getMunicipioId(localidade, uf)

            updateEvent(idAnuncio, idMunicipio, endCompleto, nome, descricao, instagram, status, space, preco, tamanhoLocal, email, telefone)

            flash("Atualizado com sucesso!")
            return redirect(url_for("editar_perfil"))
            
        else:
            return redirect(url_for("home"))
        
    except Exception as e:

        flash(f"Ocorreu um erro! {e}")
        return redirect(url_for("editar_perfil"))

@app.route("/deletar", methods=["POST"])
def deletar():

    try:

        if int(request.args["acesso"]) == 1:

            idAnuncio = request.args.get("idAnuncio")
            
            deleteEvent(idAnuncio)

            flash("Deletado com sucesso!")
            return redirect(url_for("editar_perfil"))
        
        else:
            return redirect(url_for("home"))

    except Exception as e:

            flash(f"Ocorreu um erro! {e}")
            return redirect(url_for("editar_perfil"))


@app.route("/criar_anuncio")
def criar_anuncio():
    if "loggedin" in session and session["loggedin"] is True:
        return render_template("AnunciouCriarBeta.html")
    else:
        return render_template(url_for("auth.login"))


@app.route("/criar_anuncio", methods=["POST"])
def criar_anuncio_POST():
    if request.method == "POST":
        email = session["email"]
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        tipos = request.form.getlist("tipos")
        imagens = request.files.getlist("imagem")
        local = request.form.get("localizacao")
        cep = request.form.get("localizacaocep")
        email_contato = request.form.get("email")
        telefone = request.form.get("telefone")
        instagram = request.form.get("instagram")
        espaco_bool = request.form.get("espaco")
        tamanho = request.form.get("tamanho")
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
        print("valor de diária: ", valor_diaria)

        # primeira operação de inserção
        insert_anuncio(
            email,
            estado,
            cidade,
            local,
            titulo,
            1,
            espaco_bool,
            valor_diaria,
            tamanho,
            email_contato,
            telefone,
            instagram,
            descricao
        )
        # pegar id do evento para fazer inserção em eventos_categorias e imagens
        id_anuncio = get_event_id(email, estado, cidade, local, titulo, tamanho)
        print(id_anuncio)
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

    return render_template("AnunciouCriarBeta.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port="3030")
