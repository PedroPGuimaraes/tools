import http.client
import requests
import json
import os
import secrets
import string

def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_access_token(client_id, client_secret):
    conn = http.client.HTTPSConnection("SECRET.us.auth0.com")

    payload = json.dumps({
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://dev-0xi5v04vtchrfciq.us.auth0.com/api/v2/",
        "grant_type": "client_credentials"
    })

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()
    token_info = json.loads(data.decode("utf-8"))
    return token_info.get("access_token")

def create_user(email, dashes, client_id, client_secret):
    url = "https://dev-0xi5v04vtchrfciq.us.auth0.com/api/v2/users"
    access_token = get_access_token(client_id, client_secret)

    password = generate_secure_password()

    shinyproxy_roles = dashes.split(',')

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
    print(response.text)

if __name__ == '__main__':
    email = os.environ.get('EMAIL')
    dashes = os.environ.get('DASHES')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    if not email or not dashes:
        print("Erro: EMAIL e DASHES devem ser fornecidos como variáveis de ambiente.")
    else:
        create_user(email, dashes, client_id, client_secret)