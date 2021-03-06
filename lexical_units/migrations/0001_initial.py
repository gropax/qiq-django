# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 14:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('languages', '0002_auto_20160922_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='LexicalPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LexicalUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lemma', models.CharField(max_length=80)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lexical_units', to='languages.Language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lexicalpattern',
            name='lexical_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patterns', to='lexical_units.LexicalUnit'),
        ),
        migrations.AlterUniqueTogether(
            name='lexicalunit',
            unique_together=set([('user', 'language', 'lemma')]),
        ),
    ]
