#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as f:
    README = f.read()

VERSION = "0.1.0"

setup(
    name = "python-congress",
    version = VERSION,
    description = "A Python client for the ProPublica Congress API",
    long_description = README,
    author = "Chris Amico",
    author_email = "eyeseast@gmail.com",
    py_modules = ['congress'],
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

