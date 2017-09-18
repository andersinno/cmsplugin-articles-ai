# -*- coding: utf-8 -*-
import pytest
from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from cmsplugin_articles_ai.cms_plugins import ArticleList, TagFilterArticleList, TagList
from cmsplugin_articles_ai.factories import PublicArticleFactory, TagFactory, CategoryFactory
from cmsplugin_articles_ai.models import Article
from tests.test_views import publish_articles_with_publisher


def create_articles(amount):
    for _ in range(amount):
        PublicArticleFactory()


def init_content_renderer(request=None):
    """
    Create and return `ContentRenderer` instance initiated with request.
    Request may be `None` in some cases.
    """
    return ContentRenderer(request)


def init_plugin(plugin_type, lang="en", **plugin_data):
    """
    Creates a plugin attached into a placeholder
    Returns an instance of plugin_type
    """
    placeholder = Placeholder.objects.create(slot="test")
    return add_plugin(placeholder, plugin_type, lang, **plugin_data)


@pytest.mark.django_db
def test_article_list_plugin_article_count():
    """
    Test article list plugin inserts correct amount of articles into
    the context. Amount is should be same as defined in plugin settings.
    """
    article_count = 10
    create_articles(article_count)
    publish_articles_with_publisher(Article.objects.all())
    plugin = init_plugin(ArticleList, article_amount=3)
    plugin_instance = plugin.get_plugin_class_instance()
    context = plugin_instance.render({}, plugin, None)
    assert len(context["articles"]) == 3


@pytest.mark.django_db
def test_article_list_category_exclusion():
    """
    Test article list plugin excluding articles which are within
    the excluded categories
    """
    exclude_category = CategoryFactory()
    create_articles(3)
    hidden_article = Article.objects.last()
    hidden_article.category = exclude_category
    hidden_article.save()
    publish_articles_with_publisher(Article.objects.all())
    plugin = init_plugin(ArticleList, article_amount=3)
    plugin.exclude_categories = (exclude_category,)
    plugin_instance = plugin.get_plugin_class_instance()
    context = plugin_instance.render({}, plugin, None)
    assert len(context["articles"]) == 2


@pytest.mark.django_db
def test_article_list_tag_exclusion():
    """
    Test article list plugin excluding articles which contain
    tags within the excluded tags
    """
    exclude_tag = TagFactory()
    create_articles(3)
    hidden_article = Article.objects.last()
    hidden_article.tags.add(exclude_tag)
    hidden_article.save()
    publish_articles_with_publisher(Article.objects.all())
    plugin = init_plugin(ArticleList, article_amount=3)
    plugin.exclude_tags = (exclude_tag,)
    plugin_instance = plugin.get_plugin_class_instance()
    context = plugin_instance.render({}, plugin, None)
    assert len(context["articles"]) == 2


@pytest.mark.django_db
@pytest.mark.parametrize("language_filter", ["", "en", "fi"])
def test_article_list_plugin_language_filter(language_filter):
    """
    Test article list plugin filters articles according to language filter
    """
    article_fi = PublicArticleFactory(language="fi")
    article_en = PublicArticleFactory(language="en")
    publish_articles_with_publisher(Article.objects.all())
    published_article_fi = Article.publisher_manager.published().get(language="fi")
    published_article_en = Article.publisher_manager.published().get(language="en")

    plugin = init_plugin(ArticleList, language_filter=language_filter)
    plugin_instance = plugin.get_plugin_class_instance()
    context = plugin_instance.render({}, plugin, None)
    if language_filter == "en":
        assert published_article_fi not in context["articles"]
        assert published_article_en in context["articles"]
    elif language_filter == "fi":
        assert published_article_fi in context["articles"]
        assert published_article_en not in context["articles"]
    else:
        assert published_article_fi in context["articles"]
        assert published_article_en in context["articles"]


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_plugin_html():
    """
    Test article list plugin rendering works and html has
    relevant content.
    """
    plugin = init_plugin(ArticleList)
    article = PublicArticleFactory()
    publish_articles_with_publisher([article])
    published_article = Article.publisher_manager.published().first()
    renderer = init_content_renderer()
    html = renderer.render_plugin(instance=plugin, context={}, placeholder=plugin.placeholder)
    assert published_article.title in html


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_tag_article_list_plugin_html():
    """
    Test article list plugin rendering works and html has
    relevant content.
    """
    tag = TagFactory()
    article = PublicArticleFactory(title="article1", tags=[tag])
    publish_articles_with_publisher([article])
    published_article = Article.publisher_manager.published().first()
    plugin = init_plugin(TagFilterArticleList)
    plugin.tags.add(tag)
    renderer = init_content_renderer()
    html = renderer.render_plugin(instance=plugin, context={}, placeholder=plugin.placeholder)
    assert published_article.title in html


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_tag_list_plugin_html():
    """
    Test tag list plugin rendering works and html has
    relevant content.
    """
    plugin = init_plugin(TagList)
    tag = TagFactory()
    renderer = init_content_renderer()
    html = renderer.render_plugin(instance=plugin, context={}, placeholder=plugin.placeholder)
    assert tag.name in html
