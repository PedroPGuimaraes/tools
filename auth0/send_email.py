import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email():
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    email_from = os.environ.get("EMAIL_FROM")
    password = os.environ.get("PASSWORD")
    status = os.environ.get("STATUS")
    shiny_url = os.environ.get("SHINY_URL")

    if status == "success":
        email_to = os.environ.get("EMAIL_FOR")
        email_subject = "Acesso aos dashes 4intelligence"
        html_content = f"""
            <p>Prezado, boa tarde!</p>
            <p>Segue o passo a passo para acesso à plataforma de dashes 4intelligence.</p>

            <p><strong>Usuário:</strong> {email_to}</br>
            <strong>Senha:</strong> {password}</p>

            <ol>
                <li>Acesse a URL <a href='{shiny_url}'>{shiny_url}</a> com o usuário e senha.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/1.png" alt="Login Screen" width="250"/>
                </br>
                <li>Configure o MFA (segundo fator de autenticação) lendo o QR code que será gerado usando seu app autenticador preferido.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/2.png" alt="Authenticator Screen" width="250"/>
                </br>
                <li>Troque a senha para sua segurança clicando em “forgot your password”.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/1.png" alt="Login Screen" width="250"/>
            </ol>
        """
    else:
        email_to = os.environ.get("RESPONDER")
        email_for = os.environ.get("EMAIL_FOR")
        email_subject = "Erro na criação do usuário para acesso aos dashes 4intelligence"
        html_content = f"""
            <p>Prezado, boa tarde!</p>
            <p>Houve um erro ao tentar criar o acesso para o usuário {email_for} na plataforma de dashes 4intelligence.</p>
            <p>Erro: {status}</p>
        """

    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject=email_subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Status do envio: {response.status_code}")
        print(f"Resposta: {response.body}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


if __name__ == "__main__":
    send_email()