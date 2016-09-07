# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext as _


class ArticleApp(CMSApp):
    name = _("Articles")
    urls = ["cmsplugin_articles_ai.article_urls"]


apphook_pool.register(ArticleApp)
