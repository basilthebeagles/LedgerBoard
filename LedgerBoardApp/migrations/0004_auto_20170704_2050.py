# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LedgerBoardApp', '0003_auto_20170704_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='blockHash',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='block',
            name='target',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='post',
            name='publicKeyOfSender',
            field=models.CharField(max_length=128),
        ),
    ]
