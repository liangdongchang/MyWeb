# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-12 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('SitesApp', '0013_auto_20180612_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rAddr',
            field=models.CharField(default=None, max_length=20, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rContent',
            field=tinymce.models.HTMLField(default=None, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rImpo',
            field=models.IntegerField(default=0, verbose_name='重要程度(0:一般，1:重要，3:紧急)'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rTopic',
            field=models.CharField(default=None, max_length=20, verbose_name='主题'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rUserId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SitesApp.User', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rcDateTime',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rmDateTime',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
