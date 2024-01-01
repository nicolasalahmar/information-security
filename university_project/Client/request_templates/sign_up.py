# Core
import json

# Dev
from university_project.Client.API.POST import POST


def sign_up(body):
    # start connection with the socket
    req = POST("/university/api/sign-up/", {}, json.dumps(body))

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status
