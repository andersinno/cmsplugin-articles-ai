# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from publisher.middleware import get_draft_status

from .models import Article, ArticleListPlugin, Tag


class ArticleList(CMSPluginBase):
    model = ArticleListPlugin
    module = _("Articles")
    name = _("List of latest articles")
    render_template = "cmsplugin_articles_ai/article_lift_list.html"
    fields = ["article_amount", "language_filter"]

    def get_articles(self, plugin_conf):
        return Article.objects.public(
            language=plugin_conf.language_filter,
        ).filter(publisher_is_draft=get_draft_status())

    def render(self, context, instance, placeholder):
        context.update({
            "instance": instance,
            "articles": self.get_articles(instance)[:instance.article_amount],
            "placeholder": placeholder,
        })
        return context


class TagFilterArticleList(ArticleList):
    model = ArticleListPlugin
    name = _("Tag filtered article list")
    filter_horizontal = ["tags"]
    fields = ["filter_mode", "tags", "article_amount", "language_filter"]

    def get_articles(self, plugin_conf):
        articles = super(TagFilterArticleList, self).get_articles(plugin_conf)
        return articles.tag_filter(plugin_conf.filter_mode, plugin_conf.tags)


class TagList(CMSPluginBase):
    model = CMSPlugin
    module = _("Articles")
    name = _("List of tags")
    render_template = "cmsplugin_articles_ai/tag_list.html"

    def render(self, context, *args, **kwargs):
        context["tags"] = Tag.objects.all()
        return context


plugin_pool.register_plugin(ArticleList)
plugin_pool.register_plugin(TagFilterArticleList)
plugin_pool.register_plugin(TagList)
