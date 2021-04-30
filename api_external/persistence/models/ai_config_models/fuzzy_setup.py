from django.db import models

from persistence.models.patient import Patient


class FuzzySetup(models.Model):
    universes_description = models.JSONField(null=False)
    # Essentially a list stored as json
    rules = models.JSONField(null=False)
    patient = models.OneToOneField(to=Patient, on_delete=models.CASCADE, null=True, unique=True)

    def update(self, fields_dict):
        for key, value in fields_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
