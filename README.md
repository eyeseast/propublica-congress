Python Congress
==================

This Fork
---------

This fork adds a method to access the recent votes end point of the API.

A Python client for the ProPublica [Congress API](https://projects.propublica.org/api-docs/congress-api/)

Install
-------

For this fork:

Download and run the install script:

    git clone https://github.com/astrowonk/propublica-congress.git && cd propublica-congress
    python setup.py install

Usage
-----

    >>> from congress import Congress
    >>> congress = Congress(API_KEY)
    
    # get member by bioguide ID
    >>> pelosi = congress.members.get('P000197')
    >>> pelosi['twitter_id']
    'NancyPelosi'
    
    # get recent House bills
    # recent bills come in two types: 'introduced' and 'updated'
    >>> introd = congress.bills.recent(chamber='house', congress=111, type='introduced')
    >>> len(introd['bills'])
    20
    >>> introd['chamber']
    'House'
    
    # or use a convenience function
    >>> introd = congress.bills.introduced('house')
    >>> introd['chamber']
    'House'
    >>> len(introd['bills'])
    20
    
    
