# cmsplugin-articles-ai

Articles manager for Django CMS

This CMS app provides a way to manage articles. You need to implement the frontend by yourself.

## Getting started

1. Install with pip: `pip install cmsplugin-articles-ai`
    - Note that if you want to use factories and management for generating test data, you need to install optional requirements too. You can do that either by manually
    installing them by running `pip install cmsplugin-articles-ai[utils]`
2. Add `'cmsplugin_articles_ai'` to `INSTALLED_APPS`
3. Implement frontend
    - This package includes only reference templates in (`templates/cmsplugin-articles-ai/`).
    - This package does not include any styling.

## Installing for development

Use `pip install -e /path/to/checkout` to install as "editable" package to your venv

