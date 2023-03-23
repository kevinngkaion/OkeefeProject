# Generated by Django 4.1.5 on 2023-03-23 22:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskManager', '0010_alter_task_date_created_alter_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 3, 23, 22, 30, 7, 983937, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='upload',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 22, 30, 7, 984349, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userdepartment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
