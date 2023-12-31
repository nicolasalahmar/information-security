import http
import json
from Crypto.Cipher import AES

from Authentication.enc import encrypt
from university_project.Client.key_exchange import key_exchange
from university_project.Client.request_templates.login import login
from university_project.Client.send_session_key import send_session_key_to_server
import base64
from university_project.Client.confidentiality_tools import generate_client_keys, generate_random_string, \
    get_session_key_encrypted


def achieve_confidentiality():
    host, port = '127.0.0.1', 8000
    host_port = f'{host}:{port}'

    # Authentication
    token = login({"username": "admin6", "password": "12345678"})
    if token is None:
        print('Login failed')
        return

    # Key Exchange Between Client And Server
    client_public_key = generate_client_keys().decode('utf-8')
    key_exchange_body = {
        "token": token,
        "client_public_key": client_public_key
    }
    server_public_key = key_exchange(host_port, key_exchange_body)
    print("Client Public Key :", client_public_key)
    print("Server Public Key :", server_public_key)

    # Generating Session Key, Encrypting it, Sending It to server And Receiving Response From Server
    session_key = generate_random_string(16).encode()
    print("Session Key :", session_key.decode('utf-8'))
    encrypted_session_key = get_session_key_encrypted(server_public_key, session_key)
    send_session_key_body = {
        "token": token,
        "encrypted_session_key": base64.b64encode(encrypted_session_key).decode('utf-8')
    }
    response = send_session_key_to_server(host_port, send_session_key_body)

    return session_key, token


def send_projects():
    host, port = '127.0.0.1', 8000
    host_port = f'{host}:{port}'

    session_key, token = achieve_confidentiality()

    body = {
        "Project 1": "1234567",
        "Project 2": "1234567",
    }

    cipher_body = encrypt(json.dumps(body),  session_key.decode('utf-8'))
    conn = http.client.HTTPConnection(host_port)
    headers = {"Content-Type": "application/json", "AUTHORIZATION": f"Token {token}"}
    conn.request("POST", "/university/api/send_projects/", body=cipher_body.encode(),headers=headers)

    response = conn.getresponse()

    return True


def main():
    send_projects()


if __name__ == "__main__":
    main()
