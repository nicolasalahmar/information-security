import json

from university_project.Client.API.POST import POST


def login(body):
    req = POST("/university/api/login/", {}, json.dumps(body))

    response, status = req.get_response_content()
    response = json.loads(response)

    if status == 200:
        req.close_connection()
        return response.get('token')
    else:
        req.close_connection()
        return None
