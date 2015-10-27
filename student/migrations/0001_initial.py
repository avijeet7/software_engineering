# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_auto_20151027_0524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rollno', models.CharField(max_length=15)),
                ('department', models.CharField(max_length=20)),
                ('UserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('courseid', models.ForeignKey(to='course.Catalog')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='studentcourses',
            unique_together=set([('UserId', 'courseid')]),
        ),
    ]
