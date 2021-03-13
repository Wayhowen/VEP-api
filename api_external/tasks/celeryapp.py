from celery import Celery

app = Celery('vep')
app.config_from_object('django.conf:settings', namespace='CELERY')
