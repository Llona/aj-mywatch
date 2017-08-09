# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('watch_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='add_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2017, 8, 9, 11, 0, 26, 974920)),
        ),
        migrations.AlterField(
            model_name='anime',
            name='modify_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2017, 8, 9, 11, 0, 26, 974920)),
        ),
        migrations.AlterField(
            model_name='anime',
            name='publication_date',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='anime',
            name='summary',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='anime',
            name='type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 9, 11, 0, 26, 977920)),
        ),
        migrations.AlterField(
            model_name='watchstate',
            name='watch_last_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2017, 8, 9, 11, 0, 26, 976920)),
        ),
    ]
