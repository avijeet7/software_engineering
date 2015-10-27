# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constraints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_credits', models.IntegerField(default=12)),
                ('max_credits', models.IntegerField(default=30)),
                ('max_enroll_limit_reg', models.IntegerField(default=10)),
            ],
        ),
    ]
