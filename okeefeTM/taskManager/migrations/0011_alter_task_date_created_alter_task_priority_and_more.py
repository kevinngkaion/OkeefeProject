# Generated by Django 4.1.5 on 2023-02-24 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0010_alter_task_date_completed_alter_task_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 2, 24, 23, 10, 26, 739659, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unassigned'), (1, 'Not Started'), (2, 'In Progress'), (3, 'Complete')], default=0),
        ),
    ]