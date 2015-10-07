# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readanno', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('settingid', models.IntegerField()),
                ('sequence', models.IntegerField()),
                ('taskid', models.IntegerField()),
                ('docid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taskid', models.IntegerField()),
                ('descp', models.CharField(max_length=10000)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='task',
            field=models.ForeignKey(default=0, to='readanno.Task'),
            preserve_default=False,
        ),
    ]
