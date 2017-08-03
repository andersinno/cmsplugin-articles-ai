# -*- coding: utf-8 -*-
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from cmsplugin_articles_ai import settings


def get_article_model():
    """
    Returns the Article model that is active in this project.
    """
    try:
        return apps.get_model(settings.ARTICLES_ARTICLE_MODEL)
    except ValueError:
        raise ImproperlyConfigured("ARTICLES_ARTICLE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "ARTICLES_ARTICLE_MODEL refers to model '%s' that has not been installed" % settings.ARTICLES_ARTICLE_MODEL
        )
