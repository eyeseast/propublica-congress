"""
A Python client for the New York Times Congress API
"""
import os
import urllib
import urllib2
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

class NytCongressError(Exception):
    """
    Exception for New York Times Congress API errors
    """

class Client(object):

    BASE_URI = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
    
    def __init__(self, apikey):
        self.apikey = apikey
    
    def fetch(self, path, *args, **kwargs):
        parse = kwargs.pop('parse', lambda r: r['results'])
        kwargs['api-key'] = self.apikey
        
        url = self.BASE_URI + "%s.json?" % path
        url = (url % args) + urllib.urlencode(kwargs)
        
        resp = urllib2.urlopen(url)
        result = json.load(resp)
        
        if callable(parse):
            result = parse(result)
        return result
    
    @property
    def _key(self):
        "Here for convenience"
        return urllib.urlencode({'api-key': self.apikey})
    

class MembersClient(Client):
    
    def get(self, member_id):
        path = "members/%s"
        try:
            result = self.fetch(path, member_id, parse=lambda r: r['results'][0])
            return result
        except Exception, e:
            raise NytCongressError(e)
        

class NytCongress(object):
    
    def __init__(self, apikey):
        self.apikey = apikey
        self.members = MembersClient(apikey)
    

def get_congress(year):
    "Return the Congress number for a given year"
    return (year - 1789) / 2 + 1