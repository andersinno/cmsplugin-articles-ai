# -*- coding: utf-8 -*-
from django.conf.urls import url

from cmsplugin_articles_ai.views import CategoryView
from .views import ArticleListView, ArticleView, TagFilteredArticleView

urlpatterns = [
    url(r'^tag/(?P<tag>[-_\w]+)/', TagFilteredArticleView.as_view(), name="tagged_articles"),
    url(r'^tagged/', TagFilteredArticleView.as_view(), name="tag_filtered_articles"),
    url(
        r'^category/(?P<category>[-_\w]+)/tag/(?P<tag>[-_\w]+)/',
        CategoryView.as_view(),
        name="tagged_articles_in_category"
    ),
    url(r'^category/(?P<category>[-_\w]+)/', CategoryView.as_view(), name="articles_in_category"),
    url(r'^(?P<slug>[-_\w]+)/', ArticleView.as_view(), name="article"),
    url(r'^$', ArticleListView.as_view(), name="articles"),
]
