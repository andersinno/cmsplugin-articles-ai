# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

__all__ = (
    "Category",
)


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=200)
    slug = models.SlugField(
        max_length=200,
        verbose_name=_("URL slug"),
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return the URL to the category's article list view.
        Note that this will raise NoReverseMatch if articles app hasn't
        been hooked to any CMS page.
        """
        return reverse("articles_in_category", kwargs={"category": self.slug})
