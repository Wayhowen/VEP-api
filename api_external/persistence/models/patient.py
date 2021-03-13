from datetime import date

from django.db import models

from persistence.enums import Gender


class Patient(models.Model):
    first_name = models.CharField(max_length=11)
    last_name = models.CharField(max_length=17)
    gender = models.CharField(max_length=1, choices=Gender.choices())
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=7)
    height_cm = models.IntegerField()
    weight_kg = models.FloatField(max_length=5)

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
