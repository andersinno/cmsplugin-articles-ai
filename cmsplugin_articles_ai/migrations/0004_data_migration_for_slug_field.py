# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def assign_slug_field(apps, schema_editor):
    Tag = apps.get_model("cmsplugin_articles_ai", "Tag")
    for tag in Tag.objects.all():
        tag.slug = slugify(tag.name)
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0003_add_non_unique_slug_to_tags'),
    ]

    operations = [
        migrations.RunPython(assign_slug_field),
    ]
