import http.client
import requests
import json
import os
import secrets
import string

def generate_secure_password(length=16):
    try:
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    except Exception as e:
        return False

def get_access_token(client_id, client_secret):
    try:
        conn = http.client.HTTPSConnection("development-4intelligence.us.auth0.com")
        
        payload = json.dumps({
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": "https://development-4intelligence.us.auth0.com/api/v2/",
            "grant_type": "client_credentials"
        })

        headers = {'content-type': "application/json"}
        conn.request("POST", "/oauth/token", payload, headers)
        
        res = conn.getresponse()
        data = res.read()
        
        if res.status != 200:
            return False
        
        token_info = json.loads(data.decode("utf-8"))
        return token_info.get("access_token")
    
    except Exception as e:
        return False

def create_user(email, dashes, client_id, client_secret):
    try:
        access_token = get_access_token(client_id, client_secret)
        if not access_token:
            return "Empty", "Não foi possível obter o token de acesso."

        password = generate_secure_password()
        if not password:
            return "Empty", "Não foi possível gerar a senha."

        shinyproxy_roles = json.loads(dashes)

        url = "https://development-4intelligence.us.auth0.com/api/v2/users"
        payload = json.dumps({
            "email": email,
            "password": password,
            "app_metadata": {
                "shinyproxy_roles": shinyproxy_roles
            },
            "connection": "Username-Password-Authentication"
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 201:
            return f"Erro ao criar usuário: {response.status_code} {response.text}"

        return password, "success"

    except Exception as e:
        return f"Erro ao criar usuário: {e}"

email = os.environ.get('EMAIL')
dashes = os.environ.get('DASHES')
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

password, status = create_user(email, dashes, client_id, client_secret)

print(f"{password}, {status}")