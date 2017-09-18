# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0008_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='show_in_article_list_plugin',
            field=models.BooleanField(default=True, verbose_name='show in article list plugin'),
        ),
    ]
