from Crypto.PublicKey import RSA
def generate_server_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    # with open("server_private_key.pem", "wb") as f:
    #     f.write(private_key.export_key('PEM'))
    # with open("server_public_key.pem", "wb") as f:
    #     f.write(public_key.export_key('PEM'))

    return private_key.export_key('PEM'),public_key.export_key('PEM')