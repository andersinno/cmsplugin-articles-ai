# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0008_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistplugin',
            name='exclude_categories',
            field=models.ManyToManyField(to='cmsplugin_articles_ai.Category', blank=True, related_name='_articlelistplugin_exclude_categories_+', verbose_name='exclude categories'),
        ),
        migrations.AddField(
            model_name='articlelistplugin',
            name='exclude_tags',
            field=models.ManyToManyField(to='cmsplugin_articles_ai.Tag', related_name='_articlelistplugin_exclude_tags_+', verbose_name='exclude tags'),
        ),
    ]
