from cryptography.hazmat.primitives.asymmetric import rsa

# params: void => private_key/object
def generateKeyPair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key