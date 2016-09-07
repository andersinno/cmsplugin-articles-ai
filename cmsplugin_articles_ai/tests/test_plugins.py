# -*- coding: utf-8 -*-
import pytest
from cms.api import add_plugin
from cms.models import Placeholder
from django.core.urlresolvers import reverse

from ..cms_plugins import ArticleList, TagFilterArticleList, TagList
from ..factories import NotPublicArticleFactory, PublicArticleFactory, TagFactory
from ..models import Tag, TagFilterMode


def create_articles(amount):
    for _ in range(amount):
        PublicArticleFactory()


def init_plugin(plugin_type, lang="en", **plugin_data):
    """
    Creates a plugin attached into a placeholder
    Returns an instance of plugin_type
    """
    placeholder = Placeholder.objects.create(slot="test")
    return add_plugin(placeholder, plugin_type, "en", **plugin_data)


@pytest.mark.django_db
def test_article_list_plugin_article_count():
    """
    Test article list plugin inserts correct amount of articles into
    the context. Amount is should be same as defined in plugin settings.
    """
    article_count = 10
    create_articles(article_count)
    plugin = init_plugin(ArticleList, article_amount=3)
    plugin_instance = plugin.get_plugin_class_instance()
    context = plugin_instance.render({}, plugin, None)
    assert len(context["articles"]) == 3


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
@pytest.mark.parametrize("plugin_type", [
    ArticleList,
    TagFilterArticleList,
])
def test_article_list_plugin_html(plugin_type):
    """
    Test article list plugin rendering works and html has
    relevant content.
    """
    plugin = init_plugin(plugin_type)
    article = PublicArticleFactory()
    html = plugin.render_plugin({})
    assert article.title in html


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_plugin_html():
    """
    Test tag list plugin rendering works and html has
    relevant content.
    """
    plugin = init_plugin(TagList)
    tag = TagFactory()
    html = plugin.render_plugin({})
    assert tag.name in html
