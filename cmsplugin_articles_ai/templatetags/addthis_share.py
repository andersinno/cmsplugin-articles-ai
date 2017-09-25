# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag("tags/addthis_share/addthis_share_buttons.html")
def render_addthis_share_buttons():
    return {
        "url": getattr(settings, "ADDTHIS_SHARE_BUTTONS_URL", None),
        "css_class": getattr(settings, "ADDTHIS_SHARE_BUTTONS_CSS_CLASS", None)
    }
