# -*- coding: utf-8 -*-
from django.contrib import admin
from publisher.admin import PublisherAdmin, PublisherPublishedFilter

from .models import Article, ArticleAttachment, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {
        "slug": ("name",),
    }


class ArticleAttachmentInline(admin.StackedInline):
    model = ArticleAttachment
    extra = 1
    fields = ["name", "attachment_file"]


class ArticleAdmin(PublisherAdmin):
    list_display = (
        "title",
        "slug",
        "language",
        "author",
        "published_from",
        "published_until",
        'publisher_publish',
        'publisher_status'
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    filter_horizontal = ["tags"]
    list_filter = ["language", "tags", PublisherPublishedFilter]
    inlines = [ArticleAttachmentInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["author"].initial = request.user
        return form


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
