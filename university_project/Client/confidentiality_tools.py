from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import string
import secrets
import base64

def generate_client_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    with open("client_private_key.pem", "wb") as f:
        f.write(private_key.export_key('PEM'))
    with open("client_public_key.pem", "wb") as f:
        f.write(public_key.export_key('PEM'))

    return public_key.export_key('PEM')


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def get_session_key_encrypted(server_public_key, session_key):
    server_public_key = RSA.import_key(server_public_key)
    cipher = PKCS1_OAEP.new(server_public_key)
    encrypted_session_key = cipher.encrypt(session_key)
    return encrypted_session_key

