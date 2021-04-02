import uuid

from django.db import models

from persistence.enums import JobStatus, JobType
from persistence.managers.job_manager import JobManager
from persistence.models.data_models.activity_result import ActivityResult
from persistence.models.patient import Patient


# TODO: Add jobs aggregation for users/entries


class Job(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(choices=JobType.choices())
    status = models.IntegerField(choices=JobStatus.choices(), null=False, blank=False,
                                 default=JobStatus.PENDING.value)
    patient = models.ForeignKey(to=Patient, on_delete=models.PROTECT, null=False)
    activity_result = models.ForeignKey(to=ActivityResult, on_delete=models.PROTECT, null=True)
    error_message = models.TextField(null=True, blank=True)

    start_datetime = models.DateTimeField(null=True, db_index=True)
    last_edited_datetime = models.DateTimeField(auto_now=True)
    finish_datetime = models.DateTimeField(null=True)

    objects = JobManager()

    @property
    def uid_str(self):
        return str(self.uid)

    def update(self, fields_dict):
        for key, value in fields_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
