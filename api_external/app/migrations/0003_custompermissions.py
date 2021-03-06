# Generated by Django 3.1.6 on 2021-02-21 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('sample_practitioner_perm', 'Can do practitioner stuff'), ('sample_family_perm', 'Can do family stuff'), ('sample_patient_perm', 'Can do patient stuff'), ('sample_admin_perm', 'Can do admin stuff')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
