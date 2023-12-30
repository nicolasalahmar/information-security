import http.client
import json


def login(url, body):
    conn = http.client.HTTPConnection(url)

    conn.request("POST", "/university/api/login/", body=json.dumps(body).encode(),
                 headers={"Content-Type": "application/json"})

    response = conn.getresponse()

    response_body = response.read()

    if response.status == 200:
        conn.close()
        return json.loads(response_body).get('token')
    else:
        return None
