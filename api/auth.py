from flask import (
    render_template,
    request,
    Flask,
    Blueprint,
    flash,
    url_for,
    redirect,
    session,
)
from DAO import *
from hashlib import sha256
from envio_email import gerar_codigo, enviar_email
from datetime import datetime
import re
import base64

codigos_de_verificacao = {}

auth = Blueprint("auth", __name__, template_folder="templates")
app = Flask(__name__)


@auth.route("/login")
def login():
    if "num" in session and session["num"] is 1:
        session["num"] = None
        return render_template("login.html", num=1)
    elif "num" in session and session["num"] is -1:
        session["num"] = None
        return render_template("login.html", num=-1)
    else:
        session["num"] = None
        return render_template("login.html", num=-0)


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    senha = sha256(request.form.get("senha").encode("utf-8")).hexdigest()

    count = CheckLogin(email, senha)

    # Se não logar...
    if count == 0:
        flash("Senha e/ou Email incorretos")
        session["num"] = -1
        return redirect(url_for("auth.login"))

    # se logar...
    session["loggedin"] = True
    session["id"] = selectFromWhere("tb_usuario", "user_email", email, "user_id")
    session["nome"] = selectFromWhere("tb_usuario", "user_email", email, "user_name")
    session["email"] = email

    return redirect(url_for("home"))

@auth.route("/logoff")
def logoff():
    session["loggedin"] = False
    session["id"] = None
    session["nome"] = None
    session["email"] = None

    return redirect(url_for("home"))

@auth.route("/cadastro")
def cadastro():
    if "num" in session and session["num"] is 1:
        session["num"] = None
        return render_template("Cadastro.html", num=1)
    elif "num" in session and session["num"] is -1:
        session["num"] = None
        return render_template("Cadastro.html", num=-1)
    else:
        session["num"] = None
        return render_template("Cadastro.html", num=-0)


@auth.route("/cadastro", methods=["POST"])
def registro_post():
    email = request.form.get("email")
    senha = request.form.get("senha")
    nome1 = request.form.get("nome1")
    nome2 = request.form.get("nome2")
    cpf = request.form.get("cpf")

    checkEmail = CheckCadastro("user_email", email)
    checkCPF = CheckCadastro("user_cpf", cpf)

    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        if re.match(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})", cpf):
            if checkEmail >= 1:
                flash("Email já cadastrado!")
                session["num"] = -1
                return redirect(url_for("auth.cadastro"))
            elif checkCPF >= 1:
                flash("CPF já cadastrado")
                session["num"] = -1
                return redirect(url_for("auth.cadastro"))
            elif not email or not senha or not nome1 or not nome2 or not cpf:
                flash("Preencha o formulário todo!")
                session["num"] = -1
                return redirect(url_for("auth.cadastro"))
    
            else:
                senhaHash = sha256(senha.encode("utf-8")).hexdigest()
                insertCadastro(email, senhaHash, nome1, nome2, cpf, userType='1')
                flash("Cadastrado com sucesso!")
                session["num"] = 1
                return redirect(url_for("auth.login"))
        else:
            flash("CPF inválido!")
            session["num"] = -1
            return redirect(url_for("auth.cadastro"))
    else:
        flash("Email inválido!")
        session["num"] = -1
        return redirect(url_for("auth.cadastro"))


@auth.route("/recuperar_senha")
def recuperar_senha():
    return render_template("ES_addEmail.html")


@auth.route("/recuperar_senha", methods=["POST"])
def recuperar_senha_post():
    email = request.form.get("user_email").strip()
    user_name = selectFromWhere("tb_usuario", "user_email", email, "user_name")
    count = CheckCadastro("user_email", email)

    if count >= 1:

        codigo_verificacao = gerar_codigo()
        time = datetime.now().replace(microsecond=0)
        checkCodigo = selectFromWhere(
            "tb_verificacao_senha", "user_email", email, "verification_code"
        )

        if checkCodigo is not None:
            deleteCodigo(email)

        insertCodigo(
            email, sha256(codigo_verificacao.encode("utf-8")).hexdigest(), time
        )

        envio_email = enviar_email(
            user_name, email, codigo_verificacao, time.strftime("%H:%M:%S")
        )

        if envio_email[1] == 0:
            flash(envio_email[0])
            return redirect(url_for("auth.recuperar_senha"))
        else:
            session["EmailVerificadoReset"] = True
            session["user_email"] = email

            flash(envio_email[0])
            return redirect(url_for("auth.verificar_codigo", email=email))

    else:
        flash("Email não cadastrado!")
        return redirect(url_for("auth.recuperar_senha"))


@auth.route("/verificar_codigo/<email>")
def verificar_codigo(email):
    if "EmailVerificadoReset" in session and session["EmailVerificadoReset"] is True:
        return render_template("ES_6digito.html", email=email)
    else:
        return redirect(url_for("auth.login"))


@auth.route("/verificar_codigo", methods=["POST"])
def verificar_codigo_post():
    codigo_inserido = ""
    email = session["user_email"]
    for num in range(1, 7):
        codigo_inserido += str(request.form.get(f"number_{num}"))

    codigo_gerado = selectFromWhere(
        "tb_verificacao_senha", "user_email", email, "verification_code"
    )

    if codigo_gerado == sha256(codigo_inserido.encode("utf-8")).hexdigest():
        deleteCodigo(email)
        return redirect(url_for("auth.redefinir_senha"))

    else:
        flash("Código de verificação incorreto. Por favor, tente novamente.")
        return redirect(url_for("auth.verificar_codigo", email=email))


@auth.route("/redefinir_senha")
def redefinir_senha():
    if "EmailVerificadoReset" in session and session["EmailVerificadoReset"] is True:
        return render_template("ES_TrocaSenha.html")
    else:
        return redirect(url_for("auth.login"))


@auth.route("/redefinir_senha", methods=["POST"])
def redefinir_senha_post():
    email = session["user_email"]
    senha = request.form.get("senha")
    confirmar_senha = request.form.get("confirmar_senha")
    if senha != confirmar_senha:
        flash("as senhas não coincidem")
        return redirect(url_for("auth.redefinir_senha"))
    update_senha(email, sha256(senha.encode("utf-8")).hexdigest())
    flash("senha alterada com sucesso!")
    session["EmailVerificadoReset"] = False
    session["user_email"] = None
    return redirect(url_for("auth.login"))


@auth.route("/LoadingPage1")
def LoadingPage1():
    return render_template("LoadingPage1.html")

@auth.route("/teste_blob")
def teste_blob():
    blob = selectimage(2)['event_images']
    imagem = base64.b64encode(blob).decode('utf-8')
    return render_template("modelo64.html", image_base64=imagem)
