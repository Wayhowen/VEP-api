# Generated by Django 3.1.6 on 2021-03-30 19:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0005_auto_20210326_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT,
                                    to='persistence.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='activity_result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='persistence.activityresult'),
        ),
        migrations.AlterField(
            model_name='rawrecording',
            name='file',
            field=models.FileField(upload_to='raw_recordings/', validators=[django.core.validators.RegexValidator(code='nomatch', message='The file must be of type .zip', regex='.+\\.zip$')]),
        ),
        migrations.AddField(
            model_name='activityresult',
            name='processing_result',
            field=models.JSONField(null=True),
        ),
    ]
