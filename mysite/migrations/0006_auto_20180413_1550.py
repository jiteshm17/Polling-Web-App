# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_questiontable_responsetable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsetable',
            old_name='user',
            new_name='question_id',
        ),
        migrations.AlterField(
            model_name='questiontable',
            name='category',
            field=models.CharField(default=b'general', max_length=20, choices=[(b'acedemics', b'Academics'), (b'Hostel', b'Hostel'), (b'sports', b'SPORTS'), (b'timetable', b'TIMETABLE'), (b'events', b'EVENTS'), (b'Festival', b'FESTIVAL'), (b'trip', b'TRIP'), (b'general', b'general')]),
        ),
        migrations.AlterField(
            model_name='questiontable',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'A', b'All')]),
        ),
    ]
