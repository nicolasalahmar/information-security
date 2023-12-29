import json

from http_parser.parser import HttpParser


class http_request_parser:
    def __init__(self, request_string):
        parser = HttpParser()
        parser.execute(request_string, len(request_string))

        self.method = parser.get_method()
        self.url = parser.get_url()
        self.headers = parser.get_headers()
        self.body = None

        if parser.is_partial_body():
            str = parser.recv_body()
            self.body = json.loads(str)
