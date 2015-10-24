# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('landmark_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('data', models.TextField()),
                ('duration', models.IntegerField(default=10)),
            ],
        ),
    ]
