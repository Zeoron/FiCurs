# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-30 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuaris', '0004_auto_20160527_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='monedes_pendents',
            field=models.DecimalField(decimal_places=4, default=5, max_digits=10),
        ),
    ]
