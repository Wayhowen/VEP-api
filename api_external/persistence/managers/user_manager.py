from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, user_type, relatives, assigned_practitioner_id,
                    assigned_patients, password=None):
        user = self.model(email=email, phone_number=phone_number, type=user_type)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        if relatives and user_type == "PT" or user_type == "FM":
            for relative in relatives:
                if user_type == "PT" and relative.type == "FM" or \
                        user_type == "FM" and relative.type == "PT":
                    user.relatives.add(relative)
        elif assigned_patients and user_type == "PR":
            for patient in assigned_patients:
                if patient.patient_account.type == "PT":
                    user.assigned_patients.add(patient)
        return user

    def create_superuser(self, email, phone_number, type, password):
        user = self.create_user(email, phone_number, type, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)
