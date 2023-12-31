import json

from Authentication.enc import encrypt, decrypt
from university_project.Client.API.POST import POST


def complete_sign_up(headers, body, national_id):
    body = json.dumps(body)
    cipher_body = encrypt(body, national_id)

    req = POST("/university/api/complete_sign_up/", headers, cipher_body)

    response, status = req.get_response_content()
    response = decrypt(response, national_id)
    response = json.loads(response)

    req.close_connection()
    return response, status
