# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pints_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer_Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('score_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='beer',
        ),
        migrations.RenameField(
            model_name='beer',
            old_name='style',
            new_name='beer_style',
        ),
        migrations.AddField(
            model_name='brewery',
            name='brew_type',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.AddField(
            model_name='beer_score',
            name='beer',
            field=models.ForeignKey(to='pints_main.Beer'),
        ),
    ]
