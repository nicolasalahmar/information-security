from university_project.Client.request_templates.home import home
from university_project.Client.request_templates.login import login
from university_project.Client.request_templates.sign_up import sign_up


def main():
    sign_up_creds = {
        "name": "admin4",
        "password": "12345678",
        "university": "1",
        "role": "s",
        "national_id": "1234547891"
    }
    res, status = sign_up(sign_up_creds)
    if status != 201:
        print(res)
        return

    token = login({"username": "admin4", "password": "12345678"})
    if token is None:
        print('Login failed')
        return

    home({"AUTHORIZATION": f"Token {token}"})


if __name__ == "__main__":
    main()
