# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='like_user',
            new_name='like_users',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='like_user',
            new_name='like_users',
        ),
    ]