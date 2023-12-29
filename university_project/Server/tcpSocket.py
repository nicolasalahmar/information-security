import os
import socket
import threading

import colorama

from university_project.Server.HTTP import serve_requests
from university_project.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_project.settings')
application = get_wsgi_application()


def handle_request(client_socket, host_port):
    request_data = client_socket.recv(1024)

    serve_requests(client_socket, request_data, application, host_port)

    print(colorama.Fore.RED + "closing connection" + colorama.Fore.RESET)
    client_socket.close()


def main():
    host = '127.0.0.1'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(20)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(colorama.Fore.GREEN + f"Accepted connection from {addr}" + colorama.Fore.RESET)

        client_handler = threading.Thread(target=handle_request, args=(client_socket, (host, port)))
        client_handler.start()


if __name__ == "__main__":
    main()
