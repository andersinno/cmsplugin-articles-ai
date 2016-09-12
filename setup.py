# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='cmsplugin-articles-ai',
    version='0.0.1',
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
    install_requires=open('requirements.txt').readlines(),
    extras_require=({
        'utils': ['factory-boy>=0.6.0'],
    }),
    url='https://github.com/andersinno/cmsplugin-articles-ai',
)
