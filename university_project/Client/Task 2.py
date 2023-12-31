import http.client
import json

from Authentication.enc import encrypt, decrypt
from university_project.Client.login import login


def complete_info():
    host, port = '127.0.0.1', 8000
    host_port = f'{host}:{port}'

    national_id = '12345664999'

    token = login(host_port, {"username": "admin13", "password": "12345678"})
    if token is None:
        print('Login failed')
        return

    conn = http.client.HTTPConnection(host_port)

    body = {
        "phone": "1234567",
        "mobile": "+96393123456789",
        "address": "Syria, Damascus, ..."
    }
    cipher_body = encrypt(json.dumps(body), national_id)

    headers = {"Content-Type": "application/json", "AUTHORIZATION": f"Token {token}"}

    conn.request("POST", "/university/api/complete_sign_up/", body=cipher_body.encode(),
                 headers=headers)

    response = conn.getresponse()

    response_body = response.read().decode('utf-8')
    response_body = decrypt(response_body, national_id)

    if response.status == 200:
        conn.close()
        print('response_body: ', response_body)
        return response_body
    else:
        return None


def main():
    complete_info()


if __name__ == "__main__":
    main()
