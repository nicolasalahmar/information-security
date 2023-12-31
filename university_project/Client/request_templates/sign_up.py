import http.client
import json

from university_project.Client.API.POST import POST


def sign_up(body):
    req = POST("/university/api/sign-up/", {}, json.dumps(body))

    response, status = req.get_response_content()

    req.close_connection()
    return response, status

