# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pints_main', '0007_auto_20150623_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='logo',
            field=models.ImageField(upload_to=b'profile_images', blank=True),
        ),
    ]
