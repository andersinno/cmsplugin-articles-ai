# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0005_make_tag_slug_field_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publisher_is_draft',
            field=models.BooleanField(default=True, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_linked',
            field=models.OneToOneField(null=True, related_name='publisher_draft', to='cmsplugin_articles_ai.Article', on_delete=django.db.models.deletion.SET_NULL, editable=False),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_modified_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_published_at',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
