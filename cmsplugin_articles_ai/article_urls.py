# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ArticleListView, ArticleView, TagFilteredArticleView

urlpatterns = [
    url(r'^tag/(?P<tag>[-_\w]+)/', TagFilteredArticleView.as_view(), name="tagged_articles"),
    url(r'^tagged/', TagFilteredArticleView.as_view(), name="tag_filtered_articles"),
    url(r'^(?P<slug>[-_\w]+)/', ArticleView.as_view(), name="article"),
    url(r'^$', ArticleListView.as_view(), name="articles"),
]
