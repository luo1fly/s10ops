# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='sn',
            field=models.CharField(blank=1, max_length=128, null=1),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together=set([('ip_address', 'port')]),
        ),
    ]