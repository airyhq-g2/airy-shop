# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_auto_20171129_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='slip',
            field=models.ImageField(default='../static/imgs/empty.png', max_length=500, upload_to='imgs/'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='shipping',
            field=models.CharField(default='KERRY', max_length=250),
        ),
    ]
