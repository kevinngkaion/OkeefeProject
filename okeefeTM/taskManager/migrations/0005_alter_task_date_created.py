# Generated by Django 4.1.5 on 2023-02-24 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0004_alter_task_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 2, 24, 22, 55, 36, 577234, tzinfo=datetime.timezone.utc)),
        ),
    ]