# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0009_plant_data_raining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant_data',
            name='raining',
            field=models.BooleanField(default=False),
        ),
    ]
