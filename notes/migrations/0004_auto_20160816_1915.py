# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_note_references'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='original',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='note',
            name='rank',
            field=models.IntegerField(default=1),
        ),
    ]