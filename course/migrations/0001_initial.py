# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=40)),
                ('instructor', models.CharField(max_length=40)),
                ('credits', models.SmallIntegerField(default=0)),
                ('coursetag', models.CharField(default=b'C', max_length=1)),
                ('prereq', models.CharField(default=b'', max_length=100)),
                ('max_enroll_limit', models.IntegerField(default=0)),
            ],
        ),
    ]
