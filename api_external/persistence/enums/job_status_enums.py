from persistence.utils import ChoiceEnum


class JobStatus(ChoiceEnum):
    # critical path
    PENDING = 1
    IN_PROGRESS = 2
    OK = 3

    # errors
    BAD_REQUEST = 4
    WORKER_TIMEOUT = 5
    QUEUE_TIMEOUT = 6
    SUPPLIER_ERROR = 7
    ERROR = 8
