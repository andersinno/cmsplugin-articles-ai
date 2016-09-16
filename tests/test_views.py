# -*- coding: utf-8 -*-
import pytest
from cms.api import add_plugin
from cms.models import Placeholder
from cmsplugin_articles_ai.cms_plugins import ArticleList
from cmsplugin_articles_ai.factories import NotPublicArticleFactory, PublicArticleFactory, TagFactory
from cmsplugin_articles_ai.models import Tag, TagFilterMode
from django.core.urlresolvers import reverse


def create_articles(amount):
    for _ in range(amount):
        PublicArticleFactory()


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
    url = reverse("article", kwargs={"slug": article.slug})
    response = client.get(url)
    assert response.status_code == status_code
    if status_code == 200:
        assert response.context["article"].pk == article.pk


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_view_pagination(settings, client):
    """
    Test article list view lists paginated list of articles.
    """
    create_articles(10)
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
    office_article = PublicArticleFactory(tags=[home_office])

    url = reverse("tagged_articles", kwargs={"tag": home_office.slug})
    response = client.get(url)
    assert len(response.context["articles"]) == 1
    assert response.context["articles"][0].pk == office_article.pk


@pytest.mark.urls("cmsplugin_articles_ai.article_urls")
@pytest.mark.django_db
def test_article_list_view_lang_filtering(settings, client):
    """
    Test article list view can be filtered by passing lang as url parameter.
    """
    article_en = PublicArticleFactory(language="en")
    article_fi = PublicArticleFactory(language="fi")

    url = "%s?lang=en" % reverse("articles")
    response = client.get(url)
    assert article_en in response.context["articles"]
    assert article_fi not in response.context["articles"]


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
    article1 = PublicArticleFactory(tags=[news, office])
    article2 = PublicArticleFactory(tags=[tech])

    # Test ANY filter mode with news and feedback tags
    url = "%s?%s&%s" % (
        reverse("tag_filtered_articles"),
        TagFilterMode.ANY.as_url_encoded,
        Tag.objects.filter(pk__in=[news.pk, feedback.pk]).as_url_encoded
    )
    response = admin_client.get(url)
    articles = response.context["articles"]
    assert article1 in articles
    assert article2 not in articles

    # Test ALL filter mode with news and office tags
    url = "%s?%s&%s" % (
        reverse("tag_filtered_articles"),
        TagFilterMode.ALL.as_url_encoded,
        Tag.objects.filter(pk__in=[news.pk, office.pk]).as_url_encoded
    )
    response = admin_client.get(url)
    articles = response.context["articles"]
    assert article1 in articles
    assert article2 not in articles
