from datetime import datetime
from json import JSONDecodeError

import requests

import settings


class Job:
    def __init__(self, job_id, job_type):
        self.uid = job_id
        self.type = job_type
        self.start_datetime = None
        self.finish_datetime = None
        self.status = 1

        self.url = f"{settings.API_INT_URL}/api/job/"
        self.put_url = f"{self.url}{self.uid}"

        self.data = self._get_job_data()
        self.processed_data = None

    def set_started(self):
        self.start_datetime = datetime.now()

    def set_finished(self):
        self.finish_datetime = datetime.now()

    def _get_job_data(self):
        response = requests.get(f"{self.url}{self.uid}", headers=settings.API_AUTHORIZATION_HEADER)
        try:
            data = response.json()
            self._remove_unecessary_data(data)
            return data
        except JSONDecodeError:
            print('Data recieved by the engine is not of JSON type', response.text)
        return data

    def _remove_unecessary_data(self, job_data: dict):
        job_data.pop("uid")
        job_data.pop("status")
        return job_data

    def update_job_status(self, status):
        self.status = status

    def as_json(self):
        return {
            "status": self.status,
            "start_datetime": self.start_datetime,
            "finish_datetime": self.finish_datetime
        }
