from django.db import models

from persistence.models.patient import Patient
from persistence.models.data_models.raw_recording import RawRecording


class ActivityResult(models.Model):
    feedback = models.TextField()
    raw_recording = models.ForeignKey(null=False, to=RawRecording, on_delete=models.PROTECT)
    patient = models.ForeignKey(null=False, to=Patient, on_delete=models.PROTECT)
    processing_result = models.JSONField(null=True)
