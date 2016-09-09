# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView

from .models import Article, TagFilterMode, Tag


class ArticleView(DetailView):
    """
    View for displaying single article.
    """
    model = Article
    template_name = "cmsplugin_articles_ai/article_detail.html"
    queryset = Article.objects.public()

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = self.object
        attachments = article.attachments.select_related("attachment_file")
        images = []
        non_images = []

        for attachment in article.attachments.select_related('attachment_file').all():
            (images if attachment.is_image else non_images).append(attachment)

        context.update({
            "attachments": non_images,
            "image_attachments": images,
            "tags": article.tags.select_related(),
        })
        return context


class ArticleListView(ListView):
    """
    View for listing all public articles or a list of public articles
    per tag. Lists are paginated according to settings value.
    """
    context_object_name = "articles"
    paginate_by = getattr(settings, "ARTICLES_PER_PAGE", 10)
    tag_filter = ""
    template_name = "cmsplugin_articles_ai/app_index.html"

    def get(self, request, *args, **kwargs):
        self.tag_filter = self.kwargs.get("tag", "")
        return super(ArticleListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles = Article.objects.public()
        if self.tag_filter:
            return articles.filter(tags__name=self.tag_filter)
        return articles

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context.update({
            "all_tags": Tag.objects.all(),
            "page_title": self.tag_filter or _("All articles"),
            "tag_filter": self.tag_filter,
        })
        return context


class TagFilteredArticleView(ArticleListView):
    """
    View for listing certain set of articles. The set can be customized
    with get parameters. This view is handy for creating cms plugins
    where the user can select the wanted filtering mode and relevant tags.
    """

    def get(self, request, *args, **kwargs):
        self.filter_tags = request.GET.get("filter_tags", [])
        if self.filter_tags:
            self.filter_tags = [
                int(pk, 10) for pk in self.filter_tags.split(",")
            ]
        self.filter_mode = TagFilterMode(
            int(request.GET.get("filter_mode", TagFilterMode.ALL.value))
        )
        return super(TagFilteredArticleView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles = super(TagFilteredArticleView, self).get_queryset()
        return articles.tag_filter(self.filter_mode, self.filter_tags)