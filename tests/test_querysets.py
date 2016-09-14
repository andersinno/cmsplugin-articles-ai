# -*- coding: utf-8 -*-
from datetime import timedelta

import pytest
from django.utils import timezone

from cmsplugin_articles_ai.factories import ArticleFactory, TagFactory
from cmsplugin_articles_ai.models import Article


def create_articles(amount):
    for _ in range(amount):
        ArticleFactory()


@pytest.mark.django_db
def test_article_is_public():
    past = timezone.now() - timedelta(hours=1)
    future = timezone.now() + timedelta(hours=1)
    article = ArticleFactory()

    # Test with no publish or end date
    article.published_from = None
    article.published_until = None
    article.save()
    assert article.is_public is False

    # Test with publish date in past but no end date
    article.published_from = past
    article.save()
    assert article.is_public

    # Test with end date in past
    article.published_until = past
    article.save()
    assert article.is_public is False

    # Test with publish date in past and end date in future
    article.published_until = future
    article.save()
    assert article.is_public


@pytest.mark.django_db
def test_article_public_query():
    past = timezone.now() - timedelta(hours=1)
    future = timezone.now() + timedelta(hours=1)
    published_no_lang = ArticleFactory(published_from=past, language="")
    published_fi = ArticleFactory(published_from=past, language="fi")
    published_en = ArticleFactory(published_from=past, language="en")
    draft_1 = ArticleFactory(published_from=None)
    draft_2 = ArticleFactory(published_from=future)
    draft_3 = ArticleFactory(published_until=past)

    public = Article.objects.public()
    assert published_no_lang in public
    assert published_fi in public
    assert published_en in public
    assert draft_1 not in public
    assert draft_2 not in public
    assert draft_3 not in public

    public = Article.objects.public(language="en")
    assert published_fi not in public
    assert published_en in public
    assert published_no_lang in public


@pytest.mark.django_db
def test_with_exact_tags_query():
    """Test only articles with the specific set of tags is returned"""
    tag1 = TagFactory()
    tag2 = TagFactory()
    tag3 = TagFactory()
    article1 = ArticleFactory(tags=[tag1, tag2])
    article2 = ArticleFactory(tags=[tag2, tag1])
    article3 = ArticleFactory(tags=[tag1, tag3])
    article4 = ArticleFactory(tags=[tag1])
    article5 = ArticleFactory(tags=[])
    articles = Article.objects.with_exact_tags(tags=[tag1, tag2])
    assert article1 in articles
    assert article2 in articles
    assert article3 not in articles
    assert article4 not in articles
    assert article5 not in articles


@pytest.mark.django_db
def test_with_any_of_tags_query():
    """Test only articles with any of given tags is returned"""
    tag1 = TagFactory()
    tag2 = TagFactory()
    tag3 = TagFactory()
    article1 = ArticleFactory(tags=[tag1, tag2])
    article2 = ArticleFactory(tags=[tag1])
    assert article1 in Article.objects.with_any_of_tags(tags=[tag1])
    assert article1 in Article.objects.with_any_of_tags(tags=[tag2])
    assert article1 not in Article.objects.with_any_of_tags(tags=[tag3])
    assert article1 in Article.objects.with_any_of_tags(tags=[tag1, tag3])
    assert article2 not in Article.objects.with_any_of_tags(tags=[tag2, tag3])


@pytest.mark.django_db
def test_with_all_tags_query():
    """Test only articles with all given tags is returned"""
    tag1 = TagFactory()
    tag2 = TagFactory()
    tag3 = TagFactory()
    article1 = ArticleFactory(tags=[tag1, tag2, tag3])
    article2 = ArticleFactory(tags=[tag1])
    assert article1 in Article.objects.with_all_tags(tags=[tag1, tag2, tag3])
    assert article1 in Article.objects.with_all_tags(tags=[tag2])
    assert article2 not in Article.objects.with_all_tags(tags=[tag1, tag3])
    assert article2 in Article.objects.with_all_tags(tags=[])
