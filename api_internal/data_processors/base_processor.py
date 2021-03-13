import time
from abc import abstractmethod

from dto.job import Job
from handlers.request_handler import Handler as RequestHandler
from mixins.singleton_mixin import SingletonMixin


class BaseProcessor(SingletonMixin):
    def __init__(self):
        self.request_handler = RequestHandler()

    def process(self, job: Job) -> Job:
        self._start_job(job)

        # TODO: Fake job processing for now
        time.sleep(30)
        preprocessed_data = self._preprocess_data(job.data)
        job.processed_data = self._process_data(preprocessed_data)

        self._finish_job(job)
        return job

    @abstractmethod
    def _preprocess_data(self, data):
        pass

    @abstractmethod
    def _process_data(self, data):
        pass

    def _start_job(self, job):
        job.set_started()
        job.update_job_status(2)
        self.request_handler.send_request("PUT", job.put_url, json=job.as_json())

    def _finish_job(self, job):
        job.set_finished()
        job.update_job_status(3)
        self.request_handler.send_request("PUT", job.put_url, json=job.as_json())
