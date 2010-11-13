"""
A Python client for the New York Times Congress API
"""
__author__ = "Chris Amico (eyeseast@gmail.com)"
__version__ = "0.1.0"

import datetime
import httplib2
import os
import urllib
import urllib2
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

__all__ = ('NytCongress', 'NytCongressError', 'get_congress')

def get_congress(year):
    "Return the Congress number for a given year"
    return (year - 1789) / 2 + 1

CURRENT_CONGRESS = get_congress(datetime.datetime.now().year)

class NytCongressError(Exception):
    """
    Exception for New York Times Congress API errors
    """

class Client(object):

    BASE_URI = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
    
    def __init__(self, apikey, cache='.cache'):
        self.apikey = apikey
        self.http = httplib2.Http(cache)
    
    def fetch(self, path, *args, **kwargs):
        parse = kwargs.pop('parse', lambda r: r['results'][0])
        kwargs['api-key'] = self.apikey
        
        url = self.BASE_URI + "%s.json?" % path
        url = (url % args) + urllib.urlencode(kwargs)
        
        resp, content = self.http.request(url)
        result = json.loads(content)
        
        if callable(parse):
            result = parse(result)
        return result
    
    @property
    def _key(self):
        "Here for convenience"
        return urllib.urlencode({'api-key': self.apikey})
    

class MembersClient(Client):
    
    def get(self, member_id):
        "Takes a bioguide_id, returns a legislator"
        path = "members/%s"
        result = self.fetch(path, member_id)
        return result
    
    def filter(self, chamber, congress=CURRENT_CONGRESS, **kwargs):
        "Takes a chamber, Congress, and optional state and district, returning a list of members"
        path = "%s/%s/members"
        result = self.fetch(path, congress, chamber, **kwargs)
        return result
    
    def bills(self, member_id, type='introduced'):
        "Same as BillsClient.by_member"
        path = "members/%s/bills/%s"
        result = self.fetch(path, member_id, type)
        return result

class BillsClient(Client):
    
    def by_member(self, member_id, type='introduced'):
        "Takes a bioguide ID and a type (introduced|updated|cosponsored|withdrawn), returns recent bills"
        path = "members/%s/bills/%s"
        result = self.fetch(path, member_id, type)
        return result
    
    def get(self, bill_id, congress=CURRENT_CONGRESS):
        path = "%s/bills/%s"
        result = self.fetch(path, congress, bill_id)
        return result
    
    def recent(self, chamber, congress=CURRENT_CONGRESS, type='introduced'):
        "Takes a chamber, Congress, and type (introduced|updated), returns a list of recent bills"
        path = "%s/%s/bills/%s"
        result = self.fetch(path, congress, chamber, type)
        return result
    
    def introduced(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for getting introduced bills"
        return self.recent(chamber, congress, 'introduced')
    
    def updated(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for getting updated bills"
        return self.recent(chamber, congress, 'updated')
    

class NytCongress(object):
    """
    Implements the public interface for the NYT Congress API
    
    Methods are namespaced by topic (though some have multiple access points).
    Everything returns decoded JSON, with fat trimmed.
    
    Create a new instance with your API key, or set an environment
    variable called NYT_CONGRESS_API_KEY.
    
    NytCongress uses httplib2, and caching is pluggable. By default,
    it uses httplib2.FileCache, in a directory called .cache, but it
    should also work with memcache or anything else that exposes the
    same interface as FileCache (per httplib2 docs).
    """
    
    def __init__(self, apikey=None, cache='.cache'):
        self.apikey = apikey or os.environ.get('NYT_CONGRESS_API_KEY')
        self.members = MembersClient(self.apikey, cache)
        self.bills = BillsClient(self.apikey, cache)
    

