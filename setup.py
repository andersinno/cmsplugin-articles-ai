# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='cmsplugin-articles-ai',
    version='0.2.0',
    author='Anders Innovations',
    author_email='info@anders.fi',
    packages=find_packages(
        exclude=[
            "tests",
        ],
    ),
    include_package_data=True,
    license='MIT',
    long_description=open('README.md').read(),
    description='Articles management app for Django CMS',
    install_requires=[
        'django-cms>=3.2,<3.5',
        'django-enumfields>=0.8.0',
        'django-filer>=1.2.4',
        'django-soft-choice-fields>=0.3.1',
        'djangocms_text_ckeditor>=3.0.0',
        'easy-thumbnails>=2.3',
        'django-model-publisher-ai>=0.3.1',
    ],
    extras_require=({
        'utils': ['factory-boy>=0.6.0'],
    }),
    url='https://github.com/andersinno/cmsplugin-articles-ai',
)
