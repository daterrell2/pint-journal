# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pints_main', '0002_auto_20150609_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 1, 25, 19, 214000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beer',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 1, 25, 29, 425000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 1, 25, 35, 536000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brewery',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 1, 25, 41, 336000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
