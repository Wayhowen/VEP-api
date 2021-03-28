import requests

import settings


class Handler:
    def __init__(self):
        self.types = {
            "GET": requests.get,
            "PUT": requests.put
        }

    def send_request(self, request_type: str, url: str, json=None) -> requests.Response:
        if json:
            response = self.types[request_type](url, data=json,
                                                headers=settings.API_AUTHORIZATION_HEADER)
        else:
            response = self.types[request_type](url, headers=settings.API_AUTHORIZATION_HEADER)
        return response
