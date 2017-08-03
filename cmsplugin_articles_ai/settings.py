# -*- coding: utf-8 -*-
# Since Django doesn't provide a clean way to define default values
# for app specific settings, we'll define the defaults here.
# This means that instead of using `django.conf.settings` to read the
# settings, we need to use `cmsplugin_articles_ai.settings`.
from django.conf import settings


ARTICLES_ARTICLE_MODEL = getattr(
    settings,
    'ARTICLES_ARTICLE_MODEL',
    'cmsplugin_articles_ai.Article'
)
