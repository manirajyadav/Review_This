# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_auto_20170727_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=120),
        ),
    ]
