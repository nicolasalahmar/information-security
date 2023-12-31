import http.client
import json


def send_session_key_to_server(url,body):
    conn = http.client.HTTPConnection(url)

    token = body.get('token')
    headers = {"Content-Type": "application/json", "AUTHORIZATION": f"Token {token}"}
    conn.request("POST", "/university/api/send_session_key_to_server/", body=json.dumps(body).encode(), headers=headers)

    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)
    print(response_body)
    if response.status == 200:
        conn.close()
        return response_body
    else:
        return None