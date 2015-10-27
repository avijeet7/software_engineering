# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Studenthistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roll_no', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='studentcourses',
            name='user',
            field=models.ForeignKey(to='history.Studenthistory'),
        ),
    ]
