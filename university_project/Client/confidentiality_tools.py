from Crypto.PublicKey import RSA

def generate_client_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    with open("university_project\Client\client_private_key.pem", "wb") as f:
        f.write(private_key.export_key('PEM'))
    with open("university_project\Client\client_public_key.pem", "wb") as f:
        f.write(public_key.export_key('PEM'))

    return public_key.export_key('PEM')