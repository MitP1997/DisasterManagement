# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-28 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='civilians',
            name='device_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='shelter',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='shelter',
            name='expected_capacity',
            field=models.IntegerField(default=0),
        ),
    ]
