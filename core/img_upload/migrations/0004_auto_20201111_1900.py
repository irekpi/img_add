# Generated by Django 3.1.3 on 2020-11-11 19:00

from django.db import migrations
from img_upload.models import create_plans


class Migration(migrations.Migration):
    dependencies = [
        ('img_upload', '0003_auto_20201111_1032'),
    ]

    operations = [
        migrations.RunPython(create_plans)
    ]
