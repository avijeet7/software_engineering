# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='max_enroll_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catalog',
            name='prereq',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
