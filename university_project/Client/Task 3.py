# Core
import http
import json
import base64

# Dev
from Authentication.enc import encrypt
from university_project.Client.key_exchange import key_exchange
from university_project.Client.request_templates.login import login
from university_project.Client.send_session_key import send_session_key_to_server
from university_project.Client.confidentiality_tools import generate_client_keys, generate_random_string, \
    get_session_key_encrypted
from encryption.asymmetric.key_pair_generator import generateKeyPair, exportPrivateKey, exportPublicKey, importPublicKey
from encryption.symmetric.key_generator import generateSessionKey
from encryption.asymmetric.RSA import RSAEncryption


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

    cipher_body = encrypt(json.dumps(body), session_key.decode('utf-8'))
    conn = http.client.HTTPConnection(host_port)
    headers = {"Content-Type": "application/json", "AUTHORIZATION": f"Token {token}"}
    conn.request("POST", "/university/api/send_projects/", body=cipher_body.encode(), headers=headers)

    response = conn.getresponse()

    return True


# def main():
#     send_projects()


def handshaking():
    server_url = f'127.0.0.1:8000'

    # generate client private/public keys
    client_private_key = generateKeyPair()

    # get the token from the file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    token = lines[1].split(":")[1].strip()
    file.close()

    # save private key in the client info
    file = open("./client_info/task3_client_private_key.txt", "w")
    file.truncate()
    file.writelines([exportPrivateKey(client_private_key).decode('utf-8')])
    file.close()

    # call the complete signUp function to start connection with the socket
    res, status = key_exchange(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "client_public_key": exportPublicKey(client_private_key.public_key()).decode('utf-8')
        },
    )

    # check if the exchange public key success
    if status != 200:
        print("exchange public keys Incomplete!!!")
        return

    # get the server public key & save it in the client file
    res = json.loads(res)
    file = open("./client_info/task3_server_public_key.txt", "w")
    file.truncate()
    file.writelines([res.get("server_public_key")])
    file.close()

    # generate session key & encrypt with the server public key
    session_key = generateSessionKey()
    server_public_key = importPublicKey(res.get("server_public_key").encode('utf-8'))
    encrypted_session_key = RSAEncryption.encrypt(session_key, server_public_key)

    # call the send_session_key_to_server function to start connection with the socket
    res, status = send_session_key_to_server(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "encrypted_session_key": encrypted_session_key
        },
    )

    # check if the
    if status != 200:
        print("session key acceptance Incomplete!!!")
        return

    # save the session key in the client file
    file = open("./client_info/task3_session_key.txt", "w")
    file.truncate()
    file.writelines([("session_key:" + session_key + "\n")])
    file.close()

    print(res)

    return session_key


def main():
    session_key = handshaking()


if __name__ == "__main__":
    main()
