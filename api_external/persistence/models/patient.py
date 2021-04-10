from datetime import date

from django.db import models

from persistence.enums import Gender
from persistence.models.custom_user import CustomUser


class Patient(models.Model):
    first_name = models.CharField(max_length=11, null=True)
    last_name = models.CharField(max_length=17, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices(), null=True)
    date_of_birth = models.DateField(null=True)
    postcode = models.CharField(max_length=7, null=True)
    height_cm = models.IntegerField(null=True)
    weight_kg = models.FloatField(max_length=5, null=True)

    patient_account = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False,
                                        related_name="patient")
    assigned_practitioner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True,
                                              related_name="assigned_patients")

    family_members = models.ManyToManyField(CustomUser, related_name="relatives")

    # TODO: make sure it works
    @property
    def age(self):
        today = date.today()
        born_years_ago = self.date_of_birth.date().year
        has_had_birthday = ((today.month, today.day) < (self.date_of_birth.date().month,
                                                        self.date_of_birth.date().day))
        return born_years_ago - has_had_birthday

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name} {self.last_name}"
