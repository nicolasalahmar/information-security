import http.client
import json


def sign_up(url, body):
    conn = http.client.HTTPConnection(url)

    conn.request("POST", "/university/api/sign-up/", body=json.dumps(body).encode(), headers={"Content-Type": "application/json"})

    response = conn.getresponse()

    conn.close()
    return True if response.status == 201 else None
