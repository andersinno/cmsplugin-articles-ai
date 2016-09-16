# -*- coding: utf-8 -*-
from cmsplugin_articles_ai.factories import TagFactory


def test_tag_factory_slug():
    """
    Since slug field is autofilled in django admin where the tags are
    usually created from, the Tagfactory should mimick that behavior.
    Test that the factory actually assignes the slug correctly.
    """
    tag = TagFactory.build(name="United States")
    assert tag.slug == "united-states"
