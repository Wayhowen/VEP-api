import uuid


def get_uuid4():
    return str(uuid.uuid4())


def get_shorter_array(array1, array2):
    if len(array1) > len(array2):
        return array1
    return array2
