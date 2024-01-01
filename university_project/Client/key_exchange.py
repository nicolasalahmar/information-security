# Core
import http.client
import json


def key_exchange(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/key_exchange/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status
