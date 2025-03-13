import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email():
    # Pegando as variáveis de ambiente (segurança no GitHub Actions)
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    email_from = os.environ.get("EMAIL_FROM")
    email_to = os.environ.get("EMAIL_TO")

    if not sendgrid_api_key or not email_from or not email_to:
        print("Erro: Verifique se as variáveis de ambiente estão configuradas corretamente.")
        return

    # Criando o e-mail
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject="Notificação do GitHub Actions",
        html_content="""
        <h1>O workflow foi executado com sucesso! ✅</h1>
        <p>Veja os detalhes no <a href='https://github.com'>GitHub</a>.</p>
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