# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourses',
            name='enroll_limit_status_inst',
            field=models.CharField(default=b'W', max_length=10),
        ),
        migrations.AddField(
            model_name='studentcourses',
            name='enroll_limit_status_reg',
            field=models.CharField(default=b'A', max_length=10),
        ),
    ]
