from app.utils import ChoiceEnum


class UserType(ChoiceEnum):
    PRACTITIONER = "PR"
    FAMILY_MEMBER = "FM"
    PATIENT = "PT"
    SYSTEM_ADMINISTRATOR = "SA"
