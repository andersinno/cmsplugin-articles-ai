# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import softchoice.fields.language


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_articles_ai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='language',
            field=softchoice.fields.language.LanguageField(help_text='Leave this empty if you want the article to be shown regardless of any language filters.', blank=True, verbose_name='language', max_length=10),
        ),
        migrations.AddField(
            model_name='articlelistplugin',
            name='language_filter',
            field=softchoice.fields.language.LanguageField(help_text="Select a language if you want to list only articles written in specificlanguage. If you don't select a language, the listing includes all languages.", blank=True, verbose_name='language filter', max_length=10),
        ),
    ]
