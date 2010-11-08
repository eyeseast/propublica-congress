"""
A Python client for the New York Times Congress API
"""
import os
try:
    import json
except ImportError:
    import simplejson as json

BASE_URI = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress"

class NytCongress(object):
    
    def __init__(self, apikey):
        self.apikey = apikey
    

def get_congress(year):
    "Return the Congress number for a given year"
    return (year - 1789) / 2 + 1