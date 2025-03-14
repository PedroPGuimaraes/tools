import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email():
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    email_from = os.environ.get("EMAIL_FROM")
    email_to = os.environ.get("EMAIL_TO")
    password = os.environ.get("PASSWORD")
    shiny_url = os.environ.get("SHINY_URL")

    if not sendgrid_api_key or not email_from or not email_to:
        print("Erro: Verifique se as variáveis de ambiente estão configuradas corretamente.")
        return

    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject="Acesso aos dashes 4intelligence",
        html_content=f"""
            <p>Prezado, boa tarde!</p>
            <p>Segue o passo a passo para acesso à plataforma de Dashes.</p>

            <p><strong>Usuário:</strong> {email_to}</br>
            <strong>Senha:</strong> {password}</p>

            <ol>
                <li>Acesse a URL <a href='{shiny_url}'>{shiny_url}</a> com o usuário e senha.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/1.png" alt="Login Screen"/>
                <li>Configure o MFA (segundo fator de autenticação) lendo o QR code que será gerado usando seu app autenticador preferido.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/2.png" alt="Authenticator Screen"/>
                <li>Troque a senha para sua segurança clicando em “forgot your password”.</li>
                <img src="https://storage.googleapis.com/bkt-4i-dev-frontend-4casthub/auth0_mail/1.png" alt="Login Screen"/>
            </ol>
            """
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