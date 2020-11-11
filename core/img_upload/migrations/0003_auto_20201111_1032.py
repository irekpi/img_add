# Generated by Django 3.1.3 on 2020-11-11 10:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_upload', '0002_auto_20201111_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='exp_date',
            field=models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30000), django.core.validators.MinValueValidator(30)], verbose_name='Wygaśnięcie'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='exp_date',
            field=models.BooleanField(default=False, verbose_name='Wygasanie'),
        ),
    ]