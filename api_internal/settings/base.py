from data_processors import DataProcessor, AnomalyDetector

CELERY_IMPORTS = ('tasks.async_tasks', )


CELERY_BROKER_URL = 'amqp://vep:HCL9aN7EAg46497kKJUnfm6B@rabbit'

# TODO: api external for now
API_INT_URL = 'http://api-external:8000'

# SECRET, DO NOT SHARE THIS
API_AUTHORIZATION_HEADER = {"Authorization": f"Api-Key P3wsx73U.526arP2bUKpgMrBD7IMNGIsEuMOKDmVl"}


JOB_PROCESSORS = {
    "1": DataProcessor.get_instance,
    "2": AnomalyDetector.get_instance
}
