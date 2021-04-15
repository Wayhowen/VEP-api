from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


# TODO: Change timestamps to actual dates
class RawRecording(models.Model):
    name = models.CharField(max_length=256)
    start_time = models.BigIntegerField(null=False)
    finish_time = models.BigIntegerField(null=False)
    file = models.FileField(upload_to=settings.RECORDINGS_FOLDER,
                            validators=[RegexValidator(regex='.+\.zip$',
                                                       message='The file must be of type .zip',
                                                       code='nomatch')])

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def update(self, fields_dict):
        for key, value in fields_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
