.. Python Congress documentation master file, created by
   sphinx-quickstart on Sun May 28 21:04:36 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Congress
===============

A Python client for the ProPublica `Congress
API <https://projects.propublica.org/api-docs/congress-api/>`__

Install
-------

From PyPI:

::

    pip install python-congress

Download and run the install script:

::

    git clone https://github.com/eyeseast/propublica-congress && cd propublica-congress
    python setup.py install

Usage
-----

The main entrypoint for the API is the ``Congress`` class, which is instantiated with your API key.
(Request an API key at `ProPublica's data store <https://www.propublica.org/datastore/api/propublica-congress-api>`_.)

Endpoints are organized into subclients attached to the main ``Congress`` instance. For example:

::

    >>> from congress import Congress
    >>> congress = Congress(API_KEY)

    # get member by bioguide ID
    >>> pelosi = congress.members.get('P000197')
    >>> pelosi['twitter_id']
    'NancyPelosi'

    # get recent House bills
    # recent bills come in two types: 'introduced' and 'updated'
    >>> introd = congress.bills.recent(
    ...     chamber='house', 
    ...     congress=115, 
    ...     type='introduced')

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



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
