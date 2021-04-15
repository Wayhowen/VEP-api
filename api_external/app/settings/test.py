from .base import *

# Settings to enable working without rabbitmq

BROKER_BACKEND = 'memory'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = "memory://localhost/"
