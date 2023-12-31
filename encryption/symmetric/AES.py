from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

from encryption.symmetric.key_generator import generateIv
from encryption.mac.MAC import Mac
from encryption.utils import encode64, decode64


class AESEncryption:
    @staticmethod
    # params: data/string , key/string => {ct/string , iv/string , mac/string}
    def encrypt(data, key):
        # convert key & iv to byte
        key = key.encode('utf-8')
        iv = encode64(generateIv())

        # encrypt the data using the key & iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

        # convert to string to send
        ct_str = decode64(ct_bytes)
        iv_str = decode64(iv)

        mac = Mac.generateMac(key.decode('utf-8'), ct_str, iv_str)

        # return the data {ct , iv , mac}
        encrypted_data = {'ct': ct_str, 'iv': iv_str, 'mac': mac}
        return encrypted_data

    @staticmethod
    # params: data/string , key/string , iv/string => data/string
    def decrypt(data, key, iv):
        # convert key & iv to byte
        key = key.encode('utf-8')
        iv = encode64(iv)

        # decrypt the data using key & iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = encode64(data)
        pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        decrypted_data = pt_bytes.decode('utf-8')

        # return the decrypted data
        return decrypted_data
