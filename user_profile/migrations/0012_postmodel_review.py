# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_commentmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='review',
            field=models.CharField(default='', max_length=120),
        ),
    ]
