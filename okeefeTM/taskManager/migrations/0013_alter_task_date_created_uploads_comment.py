# Generated by Django 4.1.5 on 2023-02-24 23:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskManager', '0012_alter_task_date_created_repeating_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 2, 24, 23, 29, 12, 176598, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Uploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('alt_txt', models.CharField(max_length=255)),
                ('time', models.DateTimeField(default=datetime.datetime(2023, 2, 24, 23, 29, 12, 177297, tzinfo=datetime.timezone.utc))),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='taskManager.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2023, 2, 24, 23, 29, 12, 177061, tzinfo=datetime.timezone.utc))),
                ('comment', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='taskManager.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
