# Core
import json

# Dev
from university_project.Client.API.GET import (GET)


def home(headers):
    # start connection with the socket
    req = GET("/university/api/home/", headers)

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status
