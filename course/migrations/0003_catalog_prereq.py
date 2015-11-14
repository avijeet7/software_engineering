# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20151027_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='prereq',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
