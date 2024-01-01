# Core
import json

# Dev
from university_project.Client.request_templates.home import home
from university_project.Client.request_templates.login import login
from university_project.Client.request_templates.sign_up import sign_up
from encryption.symmetric.key_generator import generateAESKey


# def main():
#     sign_up_creds = {
#         "name": "twfek1",
#         "password": "kaneki ken",
#         "university": "1",
#         "role": "s",
#         "national_id": "12345478911"
#     }
#     res, status = sign_up(sign_up_creds)
#     if status != 201:
#         print(res)
#         return
#
#     token = login({"username": "twfek", "password": "kaneki ken"})
#     if token is None:
#         print('Login failed')
#         return
#
#     home({"AUTHORIZATION": f"Token {token}"})

def main():
    # initiate the signUp info
    signUp_info = {
        "name": "Twfek Ajeneh",
        "password": "kaneki ken",
        "university": "1",
        "role": "s",
        "national_id": "11111112111"
    }

    # call the signUp function to start connection with the socket
    res, status = sign_up(signUp_info)

    # check if the signUp success or not
    if status != 201:
        print(res)
        return

    # save the symmetric key in the client file
    file = open("./client_info/task1_info.txt", "w")
    file.truncate()
    file.writelines(["symmetric_key:" + generateAESKey(signUp_info.get('national_id')) + "\n"])

    # try to login after signUp
    res, status = login({"username": "Twfek Ajeneh", "password": "kaneki ken"})

    # check if the login success or not
    if status == 200:
        print("User Login Successfully :)\n")
        file.writelines(["token:" + res.get('token') + "\n"])
        file.close()
    else:
        print("Login Filed :(")
        file.close()
        return

    # try to access the system
    res, status = home({"AUTHORIZATION": f"Token {res.get('token')}"})

    # check if the access success or not
    print("Response Status:", status)
    print("Response Body:", res)


if __name__ == "__main__":
    main()
