import smtplib
import email.mime.multipart
import email.mime.text
import email.mime.application
from random import choices
from string import digits


def gerar_codigo():
    codigo = "".join(choices(digits, k=6))
    return codigo


def enviar_email(user_name, user_email, codigo):

    corpo_email = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-mail de Verificação</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-image: url('https://cdn.discordapp.com/attachments/1221965249494909079/1228903097041158154/11.png?ex=662dbc32&is=661b4732&hm=b0cc2d1d6602c6ac53a37c65196113638fdbfc8245c35b99afcc7af8d5191d0a&'); background-size: cover; background-repeat: no-repeat; background-position: center;">
    <div style="max-width: 600px; margin: 50px auto; padding: 20px; background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #007bff; text-align: center;">E-mail de Verificação</h1>
        <p style="margin-bottom: 20px;">Olá, <strong>{user_name}</strong>,</p>
        <p style="margin-bottom: 20px;">Seu código de verificação é:</p>
        <h1><strong>{codigo}</strong></h1>
        <p>Utilize este código para completar o processo de verificação.</p>
        <p style="margin-bottom: 20px;">Se você não solicitou esta verificação, pode ignorar este e-mail.</p>
        <p>Atenciosamente,<br>Equipe de Verificação</p>
    </div>
</body>
</html>
    """

    try:
        msg = email.mime.multipart.MIMEMultipart()
        msg["Subject"] = f"Verificação de e-mail da 2gather"
        msg["From"] = "suporte2gather@gmail.com"
        msg["To"] = f"{user_email}"
        password = f"pplvuswahkimybob"
        msg.attach(email.mime.text.MIMEText(corpo_email, "html"))

        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()
        s.login(msg["From"], password)
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())
        s.quit()
        return (f"Sucesso: E-mail enviado com sucesso para {user_email}!", 1) 
    except Exception as e:
        return ( f"Oops! Parece que houve um problema ao enviar o e-mail. Por favor, tente novamente",0)

if __name__ == "__main__":
    print(enviar_email('guilherme', gerar_codigo, 'guilhermehzf@sempreceub.com'))
