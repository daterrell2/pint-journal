# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pints_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beer_id', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='beerscore',
            name='beer',
            field=models.ForeignKey(to='pints_main.Beer'),
        ),
        migrations.AlterField(
            model_name='beerscorearchive',
            name='beer',
            field=models.ForeignKey(to='pints_main.Beer'),
        ),
    ]
