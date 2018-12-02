# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20180411_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofilemodel',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]
