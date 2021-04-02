import time
import traceback
from abc import abstractmethod
from json import JSONDecodeError

import settings
from dto.job import Job
from handlers.request_handler import Handler as RequestHandler
from handlers.storage_handler import Handler as StorageHandler
from handlers.csv_handler import Handler as CSVHandler
from handlers.activity_handler import Handler as ActivityHandler
from mixins.singleton_mixin import SingletonMixin


class BaseProcessor(SingletonMixin):
    def __init__(self):
        self.request_handler = RequestHandler()
        self.storage_handler = StorageHandler()
        self.csv_handler = CSVHandler()
        self.activity_handler = ActivityHandler(self.csv_handler)

    def process(self, job: Job) -> Job:
        self._start_job(job)

        self._get_and_update_job_details(job)

        raw_data_file_location = self._get_raw_data_file(job.activity_result_id)
        data_folder_location = self.storage_handler.unzip_file(raw_data_file_location)

        try:
            activity_dict = self.activity_handler.raw_activity_to_dict(data_folder_location)
        except Exception as e:
            print(traceback.print_exc())

        # TODO: Fake job processing for now
        try:
            # time.sleep(30)
            preprocessed_data = self._preprocess_data(activity_dict)
            job.processed_data = self._process_data(preprocessed_data)
        except Exception:
            self.storage_handler.remove_folder(data_folder_location)
            job.error_message = "File management gone wrong"
            return job

        self.storage_handler.remove_folder(data_folder_location)
        self._finish_job(job)
        return job

    def _get_and_update_job_details(self, job):
        response = self.request_handler.send_request("GET", f"{job.job_url}{job.uid}")
        try:
            job_details = response.json()
        except JSONDecodeError:
            print('Data recieved by the engine is not of JSON type', response.text)
            job_details = {}
        job.set_job_details(job_details)

    def _get_raw_data_file(self, activity_result_id):
        response = self.request_handler.send_request("POST",
                                                     f"{settings.API_INT_URL}{settings.ACTIVITY_ENDPOINT}",
                                                     json={"activity_id": activity_result_id})
        filename = response.json()['raw_recordings'][0]["walk"]["file_url"]
        file_location = self.request_handler.download_file(filename)
        return file_location

    @abstractmethod
    def _preprocess_data(self, data):
        pass

    @abstractmethod
    def _process_data(self, data):
        pass

    def _start_job(self, job):
        job.set_started()
        job.update_job_status(2)
        self.request_handler.send_request("PUT", job.job_put_url, json=job.as_json())

    def _finish_job(self, job):
        job.set_finished()
        job.update_job_status(3)
        self.request_handler.send_request("PUT", job.job_put_url, json=job.as_json())
