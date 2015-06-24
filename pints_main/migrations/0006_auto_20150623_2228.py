# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pints_user', '0001_initial'),
        ('pints_main', '0005_auto_20150621_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerScoreArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('score_date', models.DateTimeField(auto_now=True)),
                ('beer', models.ForeignKey(to='pints_main.Beer')),
                ('user', models.ForeignKey(to='pints_user.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='beerscore',
            name='user',
            field=models.ForeignKey(default='', to='pints_user.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='beerscore',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterUniqueTogether(
            name='beerscore',
            unique_together=set([('beer', 'user')]),
        ),
    ]
