import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes


def decrypt(ciphertext, key):
    if len(key) < 16:
        key = key + (16 - len(key)) * 'x'

    byte_literal = key.encode('utf-8')
    cipher = AES.new(byte_literal, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))

    return unpad(decrypted, AES.block_size).decode('utf-8')


def encrypt(plaintext, key):
    if len(key) < 16:
        key = key + (16 - len(key)) * 'x'

    byte_literal = key.encode('utf-8')
    cipher = AES.new(byte_literal, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_plaintext)

    return base64.b64encode(encrypted).decode('utf-8')
