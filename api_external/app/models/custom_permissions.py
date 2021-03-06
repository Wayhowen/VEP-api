from django.db import models

# This is a dummy model class without a table in the database, made just to be able to create custom permissions, as
# django doesn't allow it without a reference to one of the existing models.
# https://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model


class CustomPermissions(models.Model):

    class Meta:

        managed = False

        default_permissions = ()

        permissions = (
            ('sample_practitioner_perm', 'Can do practitioner stuff'),
            ('sample_family_perm', 'Can do family stuff'),
            ('sample_patient_perm', 'Can do patient stuff'),
            ('sample_admin_perm', 'Can do admin stuff'),
        )
