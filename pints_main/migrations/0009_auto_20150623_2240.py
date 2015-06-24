# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pints_main', '0008_brewery_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brewery',
            name='logo',
            field=models.ImageField(upload_to=b'brewery_logos', blank=True),
        ),
    ]
