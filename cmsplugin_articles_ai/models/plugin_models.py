# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.db import models
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from softchoice.fields.language import LanguageField

from .tags import Tag

__all__ = (
    "ArticleListPlugin",
    "TagFilterMode",
)


class TagFilterMode(Enum):
    ANY = 1
    ALL = 2
    EXACT = 3

    class Labels:
        ANY = _("Match articles with any of given tags")
        ALL = _("Match articles with all given tags")
        EXACT = _("Match articles with exact given tags")

    @property
    def as_url_encoded(self):
        """Returns an URL encoded value ready to be used as GET parameter"""
        return urlencode({"filter_mode": self.value})


class ArticleListPlugin(CMSPlugin):
    """
    Plugin model for lifting articles filtered by tags.
    """
    filter_mode = EnumIntegerField(
        TagFilterMode,
        verbose_name=_(u"filter"),
        default=TagFilterMode.ANY,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
        related_name="article_list_plugins",
    )
    article_amount = models.PositiveSmallIntegerField(
        default=5,
        verbose_name=_("amount of articles"),
    )
    language_filter = LanguageField(
        verbose_name=_("language filter"),
        default="",
        blank=True,
        help_text=_(
            "Select a language if you want to list only articles written in specific"
            "language. If you don't select a language, the listing includes all languages."
        )
    )

    def __str__(self):
        return "Article list (amount: %s)" % self.article_amount

    def copy_relations(self, oldinstance):
        # This makes sure that the plugin's relations are copied during draft
        # publishing. Without this tags wouldn't be copied to the published
        # version of this object.
        # Docs: http://docs.django-cms.org/en/latest/how_to/custom_plugins.html#for-many-to-many-or-foreign-key-relations-to-other-objects  # NOQA
        self.tags = oldinstance.tags.all()
