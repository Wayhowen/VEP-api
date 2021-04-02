import requests

import settings


class Handler:
    def __init__(self):
        self.types = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put
        }

    def send_request(self, request_type: str, url: str, json=None) -> requests.Response:
        if json:
            response = self.types[request_type](url, json=json,
                                                headers=settings.API_AUTHORIZATION_HEADER)
        else:
            response = self.types[request_type](url, headers=settings.API_AUTHORIZATION_HEADER)
        return response

    def download_file(self, file_name):
        response = requests.get(f"{settings.API_INT_URL}{file_name}",
                                headers=settings.API_AUTHORIZATION_HEADER)
        file_name = file_name.split("/")[-1]

        local_file_destination = f"{settings.DATA_FOLDER}{file_name}"
        print(f"Downloading a file to: {local_file_destination}")
        with open(f"{local_file_destination}", "wb+") as file:
            file.write(response.content)
        return local_file_destination
