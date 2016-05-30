# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-06 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuaris', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='usuaris_que_tenen_aquest_element',
            field=models.ManyToManyField(related_name='elements_que_poseeix', through='usuaris.Posesio', to=settings.AUTH_USER_MODEL),
        ),
    ]
