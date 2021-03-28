from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class RawRecording(models.Model):
    name = models.CharField(max_length=256)
    start_time = models.BigIntegerField(null=False)
    finish_time = models.BigIntegerField(null=False)
    file = models.FileField(upload_to=settings.RECORDINGS_FOLDER,
                            validators=[RegexValidator(regex='.+\.zip$',
                                                       message='The file must be of type .zip',
                                                       code='nomatch')])

# TODO: Why timestamps?
