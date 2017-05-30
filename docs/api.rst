API
===

Congress
--------

.. automodule:: congress

.. autoclass:: Congress

Example: Using a custom cache object
************************************

Redis is a good option for a cache that can be shared between processes.

::

    >>> from redis import StrictRedis
    >>> from congress import Congress
    >>> db = StrictRedis()
    >>> congress = Congress(API_KEY, cache=db)
    >>> senate = congress.members.filter('senate') # hits the API, caching the result
    >>> senate = congress.members.filter('senate') # uses the cache


Members
-------

.. automodule:: congress.members

.. autoclass:: congress.members.MembersClient
    :members:


Bills
-----

.. automodule:: congress.bills

.. autoclass:: congress.bills.BillsClient
    :members:


Votes
-----

.. automodule:: congress.votes

.. autoclass:: congress.votes.VotesClient
    :members:


Committees
----------

.. automodule:: congress.committees

.. autoclass:: congress.committees.CommitteesClient
    :members:


Nominations
-----------

.. automodule:: congress.nominations

.. autoclass:: congress.nominations.NominationsClient
    :members:

