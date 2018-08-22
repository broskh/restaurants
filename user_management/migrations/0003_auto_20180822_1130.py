# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20180822_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantimage',
            name='image',
            field=models.ImageField(upload_to='2018/08/22/11/30/02/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='restaurant_information',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_management.Restaurant'),
        ),
    ]
