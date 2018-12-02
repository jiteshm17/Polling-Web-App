# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='birth_date',
            new_name='birthdate',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Student'), (2, b'Teacher'), (3, b'Supervisor')]),
        ),
    ]
