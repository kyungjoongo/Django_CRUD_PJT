# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_delete_test2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=250)),
                ('password', models.TextField(max_length=250)),
                ('sex', models.TextField(max_length=250)),
            ],
        ),
    ]
