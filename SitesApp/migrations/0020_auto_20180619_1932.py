# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-19 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SitesApp', '0019_auto_20180619_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rcDateTime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rmDateTime',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
    ]