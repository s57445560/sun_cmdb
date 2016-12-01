# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 03:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=32)),
                ('hostname', models.CharField(max_length=32)),
                ('fn', models.CharField(max_length=32)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipapp.UserInfo')),
            ],
        ),
    ]