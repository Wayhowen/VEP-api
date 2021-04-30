from persistence.utils import ChoiceEnum


class JobType(ChoiceEnum):
    DATA_PROCESSING = 1
    ANOMALY_DETECTION = 2
    PATIENT_EVALUATION = 3
