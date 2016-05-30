# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-06 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('preu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Decoracio',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elements.Element')),
                ('imatge', models.ImageField(default='/decoracio_imatges/default.png', max_length=500, upload_to='decoracio_imatges')),
                ('posicioX', models.IntegerField()),
                ('posicioY', models.IntegerField()),
            ],
            bases=('elements.element',),
        ),
        migrations.CreateModel(
            name='Peix',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elements.Element')),
                ('imatge', models.ImageField(default='/peixos_imatges/default.png', max_length=500, upload_to='peixos_imatges')),
                ('thumbnail', models.ImageField(default='/peixos_thubnails/default.png', max_length=500, upload_to='peixos_thubnails')),
                ('monedes_per_hora', models.IntegerField()),
            ],
            bases=('elements.element',),
        ),
    ]