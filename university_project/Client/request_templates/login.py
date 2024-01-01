# Core
import json

# Dev
from university_project.Client.API.POST import POST


def login(body):
    # start connection with the socket
    req = POST("/university/api/login/", {}, json.dumps(body))

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status
