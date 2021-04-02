import json
import os

import requests

import settings.base
from data_processors.base_processor import BaseProcessor
# from dto.data.accelerometer_dataset import Dataset


class AnomalyDetector(BaseProcessor):
    def __init__(self):
        super().__init__()

    def _preprocess_data(self, data):
        pass

    def _process_data(self, data):
        pass


if __name__ == "__main__":
    response = requests.post("http://0.0.0.0:8000/api/raw_recording/",
                             json={"patient_email": "default@default.com"},
                        headers=settings.base.API_AUTHORIZATION_HEADER)

    r_text = response.json()
    sample_file = r_text["raw_recordings"][-1]["walk"]["file_url"]
    f = requests.get(f"http://0.0.0.0:8000{sample_file}", headers=settings.base.API_AUTHORIZATION_HEADER)
    with open(f"{os.getcwd()}/test.zip", "wb+") as file:
        file.write(f.content)

    print(f.content)
    # d = Dataset(response.json()["data_entries"])
    # d.create_graph("Y-Axis data over time")
    # d.print_raw()
    # ad = AnomalyDetector()
    # ad._preprocess_data()