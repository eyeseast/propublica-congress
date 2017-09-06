#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.rst') as f:
    README = f.read()

VERSION = "0.3.5"

setup(
    name = "python-congress",
    packages=find_packages(exclude=['docs']),
    version = VERSION,
    description = "A Python client for the ProPublica Congress API",
    long_description = README,
    author = "Chris Amico",
    author_email = "eyeseast@gmail.com",
    url = 'https://github.com/eyeseast/propublica-congress',
    install_requires = ['httplib2', 'six'],
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    test_suite='test',
)

