from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    practitioner = Group.objects.create(name="PRACTITIONER")
    practitioner.save()
    family = Group.objects.create(name="FAMILY_MEMBER")
    family.save()
    patient = Group.objects.create(name="PATIENT")
    patient.save()
    admin = Group.objects.create(name="SYSTEM_ADMINISTRATOR")
    admin.save()



class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
