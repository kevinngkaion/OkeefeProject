# Generated by Django 4.1.5 on 2023-03-23 22:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0006_alter_task_date_created_alter_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 3, 23, 22, 27, 32, 155103, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='upload',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 22, 27, 32, 155526, tzinfo=datetime.timezone.utc)),
        ),
    ]
