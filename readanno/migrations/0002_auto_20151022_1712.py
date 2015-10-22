# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readanno', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('settingid', models.IntegerField()),
                ('taskid', models.IntegerField()),
                ('docseq', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SingleChoiceQuestionare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taskid', models.IntegerField()),
                ('title', models.IntegerField()),
                ('rightAnswer', models.IntegerField()),
                ('choices', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='SettingUnit',
        ),
        migrations.RemoveField(
            model_name='document',
            name='task',
        ),
        migrations.AddField(
            model_name='setting',
            name='taskseq',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
