# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-27 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuaris', '0003_auto_20160526_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='ultima_peticio',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
