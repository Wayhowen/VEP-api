import os

from job_processors import DataProcessor, AnomalyDetector, PatientExerciseEvaluator

CELERY_IMPORTS = ('tasks.async_tasks',)

CELERY_BROKER_URL = 'amqp://vep:HCL9aN7EAg46497kKJUnfm6B@rabbit'

API_INT_URL = 'http://api-external:8000'
JOB_ENDPOINT = '/api/job/'
ACTIVITY_ENDPOINT = '/api/activity/'
FUZZY_ENDPOINT = '/api/fuzzy_setup/'

# SECRET, DO NOT SHARE THIS

API_AUTHORIZATION_HEADER = {"Authorization": "Api-Key bqSoBsyR.wxyAcT5ploIDDeHcBJuHTrvsNNEAEecA"}

JOB_PROCESSORS = {
    "1": DataProcessor.get_instance,
    "2": AnomalyDetector.get_instance,
    "3": PatientExerciseEvaluator.get_instance,
}

DATA_FOLDER = f"{os.getcwd()}/temp/"

FILE_POINTERS = {
    "ACCELEROMETER":
        {
            "ACCELEROMETER_TIMES": int,
            "ACCELEROMETER_x": float,
            "ACCELEROMETER_y": float,
            "ACCELEROMETER_z": float
        },
    "ROTATION_VECTOR":
        {
            "ROTATION_VECTOR_TIMES": int,
            "ROTATION_VECTOR_xsine": float,
            "ROTATION_VECTOR_ysine": float,
            "ROTATION_VECTOR_zsine": float,
            "ROTATION_VECTOR_cos": float,
            "ROTATION_VECTOR_accuracy": float
        },
    "GYROSCOPE":
        {
            "GYROSCOPE_TIMES": int,
            "GYROSCOPE_x": float,
            "GYROSCOPE_y": float,
            "GYROSCOPE_z": float
        }
}
