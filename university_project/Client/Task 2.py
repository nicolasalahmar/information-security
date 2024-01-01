# Core
import http.client
import json

# Dev
from Authentication.enc import encrypt, decrypt
from university_project.Client.request_templates.complete_sign_up import complete_sign_up
from university_project.Client.request_templates.login import login
from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption
from encryption.mac.MAC import Mac


# def complete_info(token):
#     national_id = '1234567891'
#
#     body = {
#         "phone": "0988311840",
#         "mobile": "+96393123456789",
#         "address": "Syria, Damascus, ..."
#     }
#     response, status = complete_sign_up(headers={"AUTHORIZATION": f"Token {token}"}, body=body, national_id=national_id)
#
#     if status == 200:
#         print('response_body: ', response)
#         return response
#     else:
#         return None


# def main():
#
#     token = login({"username": "twfek", "password": "kaneki ken"})
#     if token is None:
#         print('Login failed')
#         return
#
#     complete_info(token)


def main():
    # read the symmetric_key & token from the client file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    symmetric_key = lines[0].split(":")[1].strip()
    token = lines[1].split(":")[1].strip()
    file.close()

    # initiate the complete signUp info
    body = {
        "phone": "0988311840",
        "mobile": "+96393123456789",
        "address": "Syria, Damascus, ..."
    }

    # generate IV to encrypt data than mac from encrypted_data
    iv = generateIv()
    encrypted_data = AESEncryption.encrypt(json.dumps(body), symmetric_key, iv)
    mac = Mac.generateMac(symmetric_key, encrypted_data, iv)

    # call the complete signUp function to start connection with the socket
    res, status = complete_sign_up(
        headers={"AUTHORIZATION": f"Token {token}"},
        body={
            "iv": iv,
            "encrypted_data": encrypted_data,
            "mac": mac
        },
    )

    # decrypt the returned response
    res = json.loads(res)
    decrypted_message = AESEncryption.decrypt(res.get("encrypted_message"), symmetric_key, res.get("iv"))

    print(status)
    print(decrypted_message)


if __name__ == "__main__":
    main()
