#!/usr/bin/env python

import nytcongress
from distutils.core import setup

README = open('README.md').read()

setup(
    name = "python-nytcongress",
    version = nytcongress.__version__,
    description = "A Python client for the New York Times Congress API",
    long_description = README,
    author = "Chris Amico",
    author_email = "eyeseast@gmail.com",
    py_modules = ['nytcongress'],
    platforms=["any"],
    classifiers=[
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
)

