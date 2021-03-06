from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def all(cls):
        return [x for x in cls]

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    @classmethod
    def names(cls):
        return tuple(x.name for x in cls)

    @classmethod
    def name_to_value(cls, name):
        for x in cls:
            if x.name == name:
                return x.value
        raise ValueError("Given name doesn't match any name from enum")

    @classmethod
    def get_name(cls, value):
        for x in cls:
            if value == x.value:
                return x.name
        raise ValueError("Given value doesn't match any value from enum")
