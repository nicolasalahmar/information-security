import http.client
import json

from Authentication.enc import encrypt, decrypt
from university_project.Client.request_templates.complete_sign_up import complete_sign_up
from university_project.Client.request_templates.login import login


def complete_info(token):
    national_id = '1234567891'

    body = {
        "phone": "0988311840",
        "mobile": "+96393123456789",
        "address": "Syria, Damascus, ..."
    }
    response, status = complete_sign_up(headers={"AUTHORIZATION": f"Token {token}"}, body=body, national_id=national_id)

    if status == 200:
        print('response_body: ', response)
        return response
    else:
        return None


def main():

    token = login({"username": "twfek", "password": "kaneki ken"})
    if token is None:
        print('Login failed')
        return

    complete_info(token)


if __name__ == "__main__":
    main()
