# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from cmsplugin_articles_ai.factories import TaggedArticleFactory


class Command(BaseCommand):

    help = "Creates published test articles with fake data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--lang",
            action="store",
            dest="language",
            default=settings.LANGUAGE_CODE,
            help="Language to be used."
        )
        parser.add_argument(
            "--amount",
            action="store",
            dest="number_of_articles",
            default=15,
            help="Amount of articles to be created."
        )

    def handle(self, *args, **options):
        language = options["language"]
        number_of_articles = int(options["number_of_articles"])

        # Activate language
        translation.activate(language)
        print("Publishing articles with language: %s" % language)

        for number, _ in enumerate(range(number_of_articles)):
            article = TaggedArticleFactory()
            print("  %s. article: %s" % (number + 1, article.title))

        translation.deactivate()