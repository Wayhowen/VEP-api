from django.contrib.auth.base_user import BaseUserManager


class JobManager(BaseUserManager):
    def create_new(self, job_type, patient, activity_result=None):
        job = self.model(type=job_type, patient_id=patient['id'], activity_result=activity_result)
        job.save(using=self._db)
        return job
