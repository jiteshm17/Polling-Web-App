# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20180413_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiontable',
            name='gender',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'A', b'All')]),
        ),
    ]
