import http.client

from university_project.Client.login import login
from university_project.Client.sign_up import sign_up as su


def sign_up(host_port):
    sign_up_creds = {
        "name": "admin13",
        "password": "12345678",
        "university": "1",
        "role": "s",
        "national_id":"12345664999"
    }

    res = su(host_port, sign_up_creds)

    if not res:
        print('Sign up failed')
        return False
    return True


def main():
    host, port = '127.0.0.1', 8000
    host_port = f'{host}:{port}'

    if not sign_up(host_port):
        return

    token = login(host_port, {"username": "admin13", "password": "12345678"})
    if token is None:
        print('Login failed')
        return

    conn = http.client.HTTPConnection(host_port)

    headers = {
        "Content-Type": "application/json",
        "AUTHORIZATION": f"Token {token}"
    }

    conn.request("GET", "/university/api/home/", headers=headers)

    response = conn.getresponse()

    print("Response Status:", response.status)
    print("Response Headers:", response.getheaders())

    response_body = response.read().decode()
    print("Response Body:", response_body)

    conn.close()


if __name__ == "__main__":
    main()
