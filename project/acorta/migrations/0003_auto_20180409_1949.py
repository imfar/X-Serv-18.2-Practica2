# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0002_auto_20180409_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('orig', models.CharField(max_length=128)),
                ('acort', models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(
            name='Urls_Acort',
        ),
        migrations.DeleteModel(
            name='Urls_Orig',
        ),
    ]
