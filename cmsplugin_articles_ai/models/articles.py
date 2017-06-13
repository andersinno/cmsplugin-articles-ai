# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from publisher.models import PublisherModel
from softchoice.fields.language import LanguageField

from .plugin_models import TagFilterMode
from .tags import Tag

__all__ = (
    "Article",
    "ArticleAttachment",
    "ArticleQuerySet",
)


def _get_tag_pks(tags):
    """
    Return an iterable of tag ids from the given iterable of tags unless
    the passed in iterable already contains ids.
    """
    if hasattr(tags, "values_list"):
        return tags.values_list("pk", flat=True)
    elif all(isinstance(item, int) for item in tags):
        # Looks like list already contains just ids
        return tags
    else:
        return [tag.pk for tag in tags]


class ArticleQuerySet(models.QuerySet):

    def public(self, language=None):
        """
        Returns articles that are considered public with given language or
        language agnostically if language isn't given.
        :params language: Language code
        :language type: Str
        """
        now = timezone.now()
        articles = self.filter(Q(published_from__lte=now) & Q(Q(published_until__gte=now) | Q(published_until=None)))
        if language:
            # Articles with blank language should be considered language agnostic.
            return articles.filter(Q(language=language) | Q(language=""))
        return articles

    def tag_filter(self, filter_mode, tags):
        """
        Filter queryset according to given filter mode and given tags.
        """
        if not isinstance(filter_mode, TagFilterMode):
            filter_mode = TagFilterMode(filter_mode)
        articles = self.all()
        if filter_mode == TagFilterMode.ANY:
            return articles.with_any_of_tags(tags)
        elif filter_mode == TagFilterMode.ALL:
            return articles.with_all_tags(tags)
        return articles.with_exact_tags(tags)

    def with_exact_tags(self, tags):
        """
        Find articles that have exactly (no more, no less) the given tags.
        :params tags: Iterable of Tags or tag ids
        """
        # Reduce the query to only articles with correct amount of tags
        tag_pks = _get_tag_pks(tags)
        articles = self.annotate(count=Count('tags')).filter(count=len(tag_pks))

        for pk in tag_pks:
            articles = articles.filter(tags__pk=pk)
        return articles

    def with_all_tags(self, tags):
        """
        Find articles that have at least the given tags.
        Article can have more tags, no less though.
        :params:
            :tags: Iterable of Tags or tag ids
        """
        # Reduce the query to only articles with correct amount of tags
        tag_pks = _get_tag_pks(tags)
        articles = self.all()

        for pk in tag_pks:
            articles = articles.filter(tags__pk=pk)
        return articles

    def with_any_of_tags(self, tags):
        """
        Find articles that have any of the given tags.
        Article can have more and less than the given tags, but it needs
        to have at least one of the given tags.
        :params:
            :tags: Iterable of Tags or tag ids
        """
        tag_pks = _get_tag_pks(tags)
        return self.filter(tags__in=tag_pks).distinct()


@python_2_unicode_compatible
class Article(PublisherModel):
    title = models.CharField(verbose_name=_("title"), max_length=200)
    slug = models.SlugField(
        max_length=200,
        verbose_name=_("URL slug"),
        db_index=True,
    )
    language = LanguageField(
        verbose_name=_("language"),
        default=settings.LANGUAGE_CODE,
        blank=True,
        help_text=_(
            "Leave this empty if you want the article to be "
            "shown regardless of any language filters."
        )
    )
    published_from = models.DateTimeField(
        _("published from"), null=True, blank=True,
    )
    published_until = models.DateTimeField(
        _("published until"), null=True, blank=True,
    )
    highlight = models.BooleanField(
        _("highlight"), default=False, help_text=_("Highlight as important."),
    )
    author = models.ForeignKey(
        User, verbose_name=_("author"), on_delete=models.PROTECT,
    )
    tags = models.ManyToManyField(
        Tag, verbose_name=_("tags"), related_name="articles", blank=True,
    )
    main_image = FilerImageField(
        verbose_name=_("main image"),
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    main_content = HTMLField(verbose_name=_("content"))

    created_at = models.DateTimeField(
        _("creation time"), auto_now_add=True, editable=False,
    )
    modified_at = models.DateTimeField(
        _("last modified"), auto_now=True, editable=False,
    )

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ('-published_from', '-pk')

    def __str__(self):
        return self.title

    @property
    def is_highlighted(self):
        return self.highlight

    @property
    def is_public(self):
        now = timezone.now()
        if not self.published_from:
            return False
        if self.published_from > now:
            return False
        if self.published_until and self.published_until < now:
            return False
        return True

    def get_absolute_url(self):
        """
        Return the URL to the article's detail view.
        Note that this will raise NoReverseMatch if articles app hasn't
        been hooked to any CMS page.
        """
        return reverse("article", kwargs={"slug": self.slug})

    def clone_relations(self, src_obj, dst_obj):
        """
        Implements cloning relations from article to another

        :param src_obj: Article object where the relations are copied from
        :param dst_obj: Article object where the relations are copied to
        """
        dst_obj.tags = src_obj.tags.all()

        for attachment in src_obj.attachments.all():
            attachment.pk = None
            attachment.article = dst_obj
            attachment.save()


class ArticleQuerySet(models.QuerySet):

    def images(self):
        return self.filter(is_image=True)

    def non_images(self):
        return self.filter(is_image=False)


class ArticleAttachment(models.Model):
    name = models.CharField(_("name"), max_length=64, blank=True)
    attachment_file = FilerFileField(
        verbose_name=_("file"),
        on_delete=models.SET(""),
    )
    article = models.ForeignKey(
        Article, verbose_name=_("article"),
        related_name="attachments",
    )
    is_image = models.BooleanField(
        default=False,
        editable=False,
        db_index=True
    )

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _("article attachment")
        verbose_name_plural = _("article attachments")

    def __str__(self):
        return "%s (%s)" % (self.name, self.filename)

    @property
    def icon_url(self):
        obj = self.attachment_file.get_real_instance()
        return obj.icons.get("16", "")

    @property
    def title(self):
        return self.name or self.filename

    @property
    def url(self):
        return self.attachment_file.url

    @property
    def size(self):
        return self.attachment_file.size

    @property
    def filename(self):
        return self.attachment_file.original_filename

    def _is_file_image(self):
        file_type = self.attachment_file.get_real_instance().file_type
        return file_type == "Image"

    def save(self, *args, **kwargs):
        self.is_image = self._is_file_image()
        return super(ArticleAttachment, self).save(*args, **kwargs)
