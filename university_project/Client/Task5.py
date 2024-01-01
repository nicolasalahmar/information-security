# Core
import json
from cryptography.hazmat.primitives import serialization

# Dev
from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption
from encryption.asymmetric.key_pair_generator import importPrivateKey, exportPublicKey
from university_project.Client.request_templates.requests_functions import send_csr
from encryption.digital_signature.DigitalSignature import DigitalSignature
from encryption.asymmetric.key_pair_generator import generateKeyPair
from encryption.digital_certificates.DigitalCertificate import DigitalCertificate


def main():
    server_url = f'127.0.0.1:8000'

    # get the token from the file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    token = lines[1].split(":")[1].strip()
    file.close()

    # generate key pair
    client_private_key = generateKeyPair()

    # create CSR
    csr = DigitalCertificate.generateCSR("Twfek Ajeneh", client_private_key)
    csr = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')

    # send CSR to the CA
    res, status = send_csr(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "csr": csr
        },
    )

    if status != 200:
        print("CSR Request failed!!!")
        return

    print(res)


if __name__ == "__main__":
    main()
