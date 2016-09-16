# -*- coding: utf-8 -*-
import random
import string
from datetime import timedelta

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from factory import fuzzy

from .models import Article, Tag


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for django.contrib.auth User model"""
    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(
        lambda user: (user.first_name + user.last_name).lower()
    )
    first_name = factory.Faker("first_name", locale='en')
    last_name = factory.Faker("last_name", locale='en')
    email = (
        factory.LazyAttribute(
            lambda user: (
                "%s.%s@example.com" % (user.first_name, user.last_name)
            ).lower()
        )
    )


class TagFactory(factory.django.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8, chars=string.ascii_letters)
    slug = factory.LazyAttribute(lambda tag: slugify(tag.name))

    class Meta:
        model = Tag


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Article

    title = factory.Faker("catch_phrase")
    slug = factory.LazyAttribute(lambda article: slugify(article.title))
    published_from = timezone.now() - timedelta(days=1)
    author = factory.SubFactory(UserFactory)
    main_content = factory.Faker(
        "paragraph",
        nb_sentences=10,
        variable_nb_sentences=True,
        locale="en"
    )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # A list of groups were passed in, use them
        for tag in (extracted or []):
            self.tags.add(tag)


class PublicArticleFactory(ArticleFactory):
    pass


class NotPublicArticleFactory(ArticleFactory):
    published_from = None


class TaggedArticleFactory(ArticleFactory):

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
        else:
            for _ in range(random.randrange(0, 5)):
                self.tags.add(TagFactory())
