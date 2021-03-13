from django.contrib.auth.base_user import BaseUserManager
from django.utils.timezone import now


class JobManager(BaseUserManager):
    def create_new(self, type):
        job = self.model(type=type)
        job.save(using=self._db)
        return job

    def get_and_update(self, pk, fields_to_update):
        job = self.get(pk=pk)
        self.update_time_field(job, fields_to_update)
        return job

    @staticmethod
    def update_time_field(instance, time_fields):
        for field in time_fields:
            setattr(instance, field, now())
        instance.save()
