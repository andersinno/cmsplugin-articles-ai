# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0006_add_publisher_support'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': (('can_publish', 'Can publish'),), 'verbose_name_plural': 'articles', 'ordering': ('-published_from', '-pk'), 'verbose_name': 'article'},
        ),
        migrations.AddField(
            model_name='article',
            name='lead_paragraph',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, verbose_name='lead paragraph'),
        ),
    ]
