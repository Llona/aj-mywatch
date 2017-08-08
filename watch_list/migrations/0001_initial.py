# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('origin_name', models.CharField(max_length=100, blank=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('media_type', models.CharField(max_length=50, blank=True)),
                ('type', models.CharField(max_length=20, blank=True)),
                ('publication_date', models.CharField(max_length=20, blank=True)),
                ('url', models.CharField(max_length=300, blank=True)),
                ('cover', models.ImageField(upload_to='covers/', blank=True, null=True)),
                ('summary', models.TextField(max_length=2000, blank=True)),
                ('modify_date', models.DateTimeField(default=datetime.datetime(2017, 8, 8, 15, 55, 56, 622435), null=True)),
                ('add_date', models.DateTimeField(default=datetime.datetime(2017, 8, 8, 15, 55, 56, 622435), null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 8, 8, 15, 55, 56, 625435))),
                ('news_type', models.CharField(max_length=50, blank=True)),
                ('content', models.CharField(max_length=500, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/', blank=True, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchState',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('watch_last_date', models.DateTimeField(default=datetime.datetime(2017, 8, 8, 15, 55, 56, 624435), null=True)),
                ('num_of_chapter', models.CharField(max_length=50, blank=True)),
                ('watch_state', models.IntegerField(default=1)),
                ('anime', models.ForeignKey(to='watch_list.Anime')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='watch_state',
            field=models.ManyToManyField(through='watch_list.WatchState', to=settings.AUTH_USER_MODEL),
        ),
    ]
