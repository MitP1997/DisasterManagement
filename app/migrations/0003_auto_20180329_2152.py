# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-29 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180328_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='civilians',
            name='aadhar_number',
            field=models.IntegerField(unique=True),
        ),
    ]
