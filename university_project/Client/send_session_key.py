# Core
import http.client
import json


def send_session_key_to_server(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/send_session_key_to_server/",
        body=json.dumps(body),
        headers=headers
    )

    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status
