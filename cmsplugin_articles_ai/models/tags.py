# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

__all__ = (
    "Tag",
    "TagQuerySet",
)


class TagQuerySet(models.QuerySet):

    @property
    def as_url_encoded(self):
        """
        Return queryset as URL encoded string that is compatible with
        the article views.
        """
        tag_pks = list(sorted(self.values_list("pk", flat=True)))
        return urlencode({
            "filter_tags": ",".join(str(pk) for pk in tag_pks),
        })


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=200, unique=True)
    slug = models.SlugField(verbose_name=_("slug"), max_length=200, unique=True)
    objects = TagQuerySet.as_manager()

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        ordering = ('name',)

    def __str__(self):
        return self.name
