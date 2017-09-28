# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0009_auto_20170919_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlelistplugin',
            name='exclude_tags',
            field=models.ManyToManyField(blank=True, to='cmsplugin_articles_ai.Tag', related_name='_articlelistplugin_exclude_tags_+', verbose_name='exclude tags'),
        ),
    ]
