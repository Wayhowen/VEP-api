import json

from rest_framework import parsers


# Class created in order to be able to add JSON to multipart data, in accordance with
# https://stackoverflow.com/questions/30176570/using-django-rest-framework-how-can-i-upload-a-file-and-send-a-json-payload


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if not isinstance(value, str):
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value
        return parsers.DataAndFiles(data, result.files)
