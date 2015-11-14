# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prerequisites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prereq', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='prereq',
        ),
        migrations.AddField(
            model_name='prerequisites',
            name='cid',
            field=models.ForeignKey(to='course.Catalog'),
        ),
    ]
