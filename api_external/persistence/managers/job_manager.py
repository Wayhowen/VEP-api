from django.contrib.auth.base_user import BaseUserManager


class JobManager(BaseUserManager):
    def create_new(self, type, patient, activity_result=None):
        job = self.model(type=type, patient_id=patient['id'], activity_result=activity_result)
        job.save(using=self._db)
        return job
