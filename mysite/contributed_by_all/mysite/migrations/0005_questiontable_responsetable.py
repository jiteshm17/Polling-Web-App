# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20180411_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=100)),
                ('question_text_undrscr', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('category', models.CharField(default=b'general', max_length=20, choices=[(b'acedemics', b'Acedemics'), (b'Hostel', b'Hostel'), (b'sports', b'SPORTS'), (b'timetable', b'TIMETABLE'), (b'events', b'EVENTS'), (b'Festival', b'FESTIVAL'), (b'trip', b'TRIP'), (b'general', b'general')])),
                ('yes_vote', models.PositiveIntegerField(default=0)),
                ('no_vote', models.PositiveIntegerField(default=0)),
                ('dontcare_vote', models.PositiveIntegerField(default=0)),
                ('confused_vote', models.PositiveIntegerField(default=0)),
                ('dead_line', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ResponseTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voter_id', models.PositiveIntegerField(default=1)),
                ('choice', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(to='mysite.QuestionTable')),
            ],
        ),
    ]
