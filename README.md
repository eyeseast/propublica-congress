Python NytCongress
==================

A Python client for the New York Times [Congress API](http://developer.nytimes.com/docs/congress_api)

Install
-------

    $ pip install python-nytcongress

Or download and run

    $ python setup.py install

Usage
-----

    >>> from nytcongress import NytCongress
    >>> congress = NytCongress(API_KEY)
    
    # get member by bioguide ID
    >>> pelosi = congress.members.get('P000197')