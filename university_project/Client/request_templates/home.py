import json

from university_project.Client.API.GET import GET


def home(headers):
    req = GET("/university/api/home/", headers)

    response, status = req.get_response_content()

    print("Response Status:", status)

    response = json.loads(response)
    print("Response Body:", response)

    req.close_connection()
    return response

