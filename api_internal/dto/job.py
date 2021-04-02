from datetime import datetime

import settings


class Job:
    def __init__(self, job_id, job_type):
        self.uid = job_id
        self.type = job_type
        self.start_datetime = None
        self.finish_datetime = None
        self.status = 1
        self.error_message = None
        self.patient_id = None
        self.activity_result_id = None

        self.job_url = f"{settings.API_INT_URL}{settings.JOB_ENDPOINT}"
        self.job_put_url = f"{self.job_url}{self.uid}"

    def set_started(self):
        self.start_datetime = datetime.now()

    def set_finished(self):
        self.finish_datetime = datetime.now()

    def set_job_details(self, job_details):
        processed_job_details = self._remove_unecessary_data(job_details)
        self.patient_id = processed_job_details.get("patient_id", None)
        self.activity_result_id = processed_job_details.get("activity_result_id", None)
        return processed_job_details

    def _remove_unecessary_data(self, job_data: dict):
        job_data.pop("uid")
        job_data.pop("status")
        return job_data

    def update_job_status(self, status):
        self.status = status

    def as_json(self):
        job_json = {
            "status": self.status
        }
        if self.start_datetime:
            job_json["start_datetime"] = self.start_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        if self.finish_datetime:
            job_json["finish_datetime"] = self.finish_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        return job_json
