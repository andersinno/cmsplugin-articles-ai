# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='cmsplugin-articles-ai',
    version='0.0.1',
    author='Anders Innovations',
    author_email='info@anders.fi',
    packages=[
        'cmsplugin_articles_ai',
        'cmsplugin_articles_ai.management',
        'cmsplugin_articles_ai.migrations',
        'cmsplugin_articles_ai.templates',
    ],
    include_package_data=True,
    license='MIT',
    long_description=open('README.md').read(),
    description='Image carousel plugin for Django CMS',
    install_requires=open('requirements.txt').readlines(),
    url='https://github.com/andersinno/cmsplugin-articles-ai',
)
