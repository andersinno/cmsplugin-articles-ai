# -*- coding: utf-8 -*-
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from django.contrib import admin

from .models import Article, ArticleAttachment, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ArticleAttachmentInline(admin.StackedInline):
    model = ArticleAttachment
    extra = 1
    fields = ["name", "attachment_file"]


class ArticleAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ("title", "author", "slug", "published_from", "published_until",)
    prepopulated_fields = {
        "slug": ("title",),
    }
    filter_horizontal = ["tags"]
    list_filter = ["tags"]
    inlines = [ArticleAttachmentInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["author"].initial = request.user
        return form


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
