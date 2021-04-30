from django.db import models

from persistence.models.patient import Patient
from persistence.models.data_models.raw_recording import RawRecording


class ActivityResult(models.Model):
    feedback = models.TextField(null=True)
    raw_recording = models.ForeignKey(null=False, to=RawRecording, on_delete=models.CASCADE,
                                      related_name="activity_result")
    patient = models.ForeignKey(null=False, to=Patient, on_delete=models.PROTECT,
                                related_name="activity_results")
    preprocessing_result = models.JSONField(null=True)
    processing_result = models.JSONField(null=True)

    def delete(self, using=None, keep_parents=None):
        self.raw_recording.delete()
        super().delete(using, keep_parents)

    def update(self, fields_dict):
        for key, value in fields_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
