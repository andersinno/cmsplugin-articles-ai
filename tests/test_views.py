# -*- coding: utf-8 -*-
import pytest

from cmsplugin_articles_ai.factories import (
    CategoryFactory, NotPublicArticleFactory, PublicArticleFactory,
    TagFactory
)
from cmsplugin_articles_ai.models import Article, Tag, TagFilterMode
from django.core.urlresolvers import reverse


def create_articles(amount):
    for _ in range(amount):
        PublicArticleFactory()


def publish_articles_with_publisher(articles):
    for article in articles:
        article.publish()


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
@pytest.mark.parametrize("article_factory, status_code", [
    (PublicArticleFactory, 200,),
    (NotPublicArticleFactory, 404,)
])
def test_article_detail_view(client, article_factory, status_code):
    """
    Test article list view lists paginated list of articles.
    """
    article = article_factory()
    article.publish()

    url = reverse("article", kwargs={"slug": article.slug})
    response = client.get(url)
    assert response.status_code == status_code
    if status_code == 200:
        published_article = Article.publisher_manager.published().first()
        assert response.context["article"].pk == published_article.pk


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_view_pagination(settings, client):
    """
    Test article list view lists paginated list of articles.
    """
    create_articles(10)
    publish_articles_with_publisher(Article.objects.all())

    url = reverse("articles")
    response = client.get(url)
    assert len(response.context["articles"]) == settings.ARTICLES_PER_PAGE


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_view_tag_filtering(settings, client):
    """
    Test article list view can be filtered by passing tag as url parameter.
    """
    news = TagFactory(name="news")
    home_office = TagFactory(name="home office")
    PublicArticleFactory(tags=[news])
    PublicArticleFactory(title="office_article", tags=[home_office])

    publish_articles_with_publisher(Article.objects.all())

    url = reverse("tagged_articles", kwargs={"tag": home_office.slug})
    response = client.get(url)
    published_office_article = Article.publisher_manager.published().get(title="office_article")
    assert len(response.context["articles"]) == 1
    assert response.context["articles"][0].pk == published_office_article.pk


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_view_lang_filtering(settings, client):
    """
    Test article list view can be filtered by passing lang as url parameter.
    """
    PublicArticleFactory(language="en")
    PublicArticleFactory(language="fi")

    publish_articles_with_publisher(Article.objects.all())

    url = "%s?lang=en" % reverse("articles")
    response = client.get(url)
    published_article_en = Article.publisher_manager.published().get(language="en")
    published_article_fi = Article.publisher_manager.published().get(language="fi")
    assert published_article_en in response.context["articles"]
    assert published_article_fi not in response.context["articles"]


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_tag_filtered_article_list_view(admin_client):
    """
    Test tag filtered article view accepts tags and filter mode
    as URL parameters and filters the list of articles accordingly.
    """
    news = TagFactory(name="news")
    office = TagFactory(name="office")
    tech = TagFactory(name="tech")
    feedback = TagFactory(name="feedback")
    PublicArticleFactory(title="article1", tags=[news, office])
    PublicArticleFactory(title="article2", tags=[tech])

    publish_articles_with_publisher(Article.objects.all())
    published_article1 = Article.publisher_manager.published().get(title="article1")
    published_article2 = Article.publisher_manager.published().get(title="article2")

    # Test ANY filter mode with news and feedback tags
    url = "%s?%s&%s" % (
        reverse("tag_filtered_articles"),
        TagFilterMode.ANY.as_url_encoded,
        Tag.objects.filter(pk__in=[news.pk, feedback.pk]).as_url_encoded
    )
    response = admin_client.get(url)
    articles = response.context["articles"]
    assert published_article1 in articles
    assert published_article2 not in articles

    # Test ALL filter mode with news and office tags
    url = "%s?%s&%s" % (
        reverse("tag_filtered_articles"),
        TagFilterMode.ALL.as_url_encoded,
        Tag.objects.filter(pk__in=[news.pk, office.pk]).as_url_encoded
    )
    response = admin_client.get(url)
    articles = response.context["articles"]
    assert published_article1 in articles
    assert published_article2 not in articles


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_category_detail_view(client):
    """
    Test category detail view article list.
    """
    category = CategoryFactory()
    article1 = PublicArticleFactory(category=category)
    article2 = PublicArticleFactory(category=None)
    publish_articles_with_publisher(Article.objects.all())

    # Double check that article categories are set up correctly.
    assert category == article1.category
    assert not article2.category

    published_article1 = Article.publisher_manager.published().get(title=article1.title)
    published_article2 = Article.publisher_manager.published().get(title=article2.title)

    response = client.get(category.get_absolute_url())
    articles = response.context["articles"]
    assert len(articles) == 1
    assert published_article1 in articles
    assert published_article2 not in articles
