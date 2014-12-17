#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as f:
    README = f.read()

VERSION = "0.1.1"

setup(
    name = "python-nytcongress",
    version = VERSION,
    description = "A Python client for the New York Times Congress API",
    long_description = README,
    author = "Chris Amico",
    author_email = "eyeseast@gmail.com",
    py_modules = ['nytcongress'],
    install_requires = ['httplib2'],
    platforms= ['any'],
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

