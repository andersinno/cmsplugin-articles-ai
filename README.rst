=====================
cmsplugin-articles-ai
=====================

Articles manager for Django CMS

This CMS app provides a way to manage articles. You need to implement the frontend by yourself.


Getting started
---------------

1. Install with pip: ``pip install cmsplugin-articles-ai``
    - Note that if you want to use factories and management for generating test data, you need
      to install optional requirements too. You can do that either by manually installing them
      by running ``pip install cmsplugin-articles-ai[utils]``
2. Add ``'cmsplugin_articles_ai'`` and ``'publisher'`` to ``INSTALLED_APPS``
3. Add ``'publisher.middleware.PublisherMiddleware'`` to ``MIDDLEWARE_CLASSES``
4. Implement frontend
    - This package includes only reference templates in (``templates/cmsplugin-articles-ai/``).
    - This package does not include any styling.


Features
--------

**Attachments**
    Articles can have file attachments. The attachments can be image or pdf for example.

**Categories**
    Articles can be categorized. Categories have their own list views that list the articles
    belonging in that article. Categories can be filtered by tags.

**Publish states**
    Articles can have saved drafts which are not public. Draft can be published from admin
    interface with a push of a button.

**Tags**
    Articles can be tagged and lists filtered by tags. Article can have any number of tags.


Usage
-----

You will see additional publish workflow buttons in the article edit page.
Article needs to be saved before you can preview the changes by clicking "Preview Draft" button
in the top bar. You need to be logged in as staff user and have edit mode on when previewing the changes.
If you are happy with the changes, go to the article edit page and click "Publish Draft" button.
Changes will be visible to anonymous users only after publishing the draft.

If you are updating existing project which has articles in the database already, you can use
``python manage.py publish_model cmsplugin_articles_ai.models.Article`` command to generate
published versions for all of them. Without a published version, article is not visible
to anonymous users!


AddThis integration
-------------------

There is support for including AddThis social share buttons using ``{% load addthis_share %}`` and
then a ``{% render_addthis_share_buttons %}`` tag. Look for the usage example in the included
template (``templates/cmsplugin_articles_ai/article_detail.html``).

To enable this add the following declarations with your AddThis details to your project's ``settings.py``:

| ``ADDTHIS_SHARE_BUTTONS_URL = "//s7.addthis.com/js/300/addthis_widget.js#pubid=..."``
| ``ADDTHIS_SHARE_BUTTONS_CSS_CLASS = "addthis_sharing_toolbox"``
|
NOTE: Set ``ADDTHIS_SHARE_BUTTONS_URL`` so that it contains the URL provided by AddThis. Not the entire
HTML snippet, just the URL inside src="...". ``ADDTHIS_SHARE_BUTTONS_CSS_CLASS`` should contain name
of the CSS class also provided by AddThis. This varies depending on which type of widget you chose.


Installing for development
--------------------------

Use ``pip install -e /path/to/checkout`` to install as "editable" package to your venv
