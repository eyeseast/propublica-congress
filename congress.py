"""
A Python client for the ProPublica Congress API

API docs: https://propublica.github.io/congress-api-docs/
"""
__author__ = "Chris Amico (eyeseast@gmail.com)"
__version__ = "0.2.0"

import datetime
import json
import os
import urllib

import httplib2

__all__ = ('Congress', 'CongressError', 'NotFound', 'get_congress', 'CURRENT_CONGRESS')


DEBUG = True

def get_congress(year):
    "Return the Congress number for a given year"
    if year < 1789:
        raise CongressError('There was no Congress before 1789.')

    return (year - 1789) / 2 + 1

def check_chamber(chamber):
    "Validate that chamber is house or senate"
    if str(chamber).lower() not in ('house', 'senate'):
        raise TypeError('chamber must be either "house" or "senate"')

def parse_date(s):
    """
    Parse a date using dateutil.parser.parse if available,
    falling back to datetime.datetime.strptime if not
    """
    if isinstance(s, (datetime.datetime, datetime.date)):
        return s
    try:
        from dateutil.parser import parse
    except ImportError:
        parse = lambda d: datetime.datetime.strptime(d, "%Y-%m-%d")
    return parse(s)

CURRENT_CONGRESS = get_congress(datetime.datetime.now().year)

# Error classes

class CongressError(Exception):
    """
    Exception for general Congress API errors
    """
    def __init__(self, message, response=None, url=None):
        super(CongressError, self).__init__(message)
        self.message = message
        self.response = response
        self.url = url


class NotFound(CongressError):
    """
    Exception for things not found
    """

# Clients

class Client(object):
    
    BASE_URI = "https://api.propublica.org/congress/v1/"
    
    def __init__(self, apikey=None, cache='.cache'):
        self.apikey = apikey
        self.http = httplib2.Http(cache)
    
    def fetch(self, path, parse=lambda r: r['results'][0]):
        """
        Make an API request, with authentication
        """
        url = self.BASE_URI + path
        headers = {'X-API-Key': self.apikey}

        resp, content = self.http.request(url, headers=headers)
        content = json.loads(content)

        # handle errors
        if not content.get('status') == 'OK':

            if "errors" in content and content['errors'][0]['error'] == "Record not found":
                raise NotFound(path)

            raise CongressError(content, resp, url)

        if callable(parse):
            content = parse(content)

        return content


class MembersClient(Client):
    
    def get(self, member_id):
        "Takes a bioguide_id, returns a legislator"
        path = "members/{0}.json".format(member_id)
        return self.fetch(path)
    
    def filter(self, chamber, congress=CURRENT_CONGRESS, **kwargs):
        """
        Takes a chamber and Congress, 
        OR state and district, returning a list of members
        """
        check_chamber(chamber)

        kwargs.update(chamber=chamber, congress=congress)

        if 'state' in kwargs and 'district' in kwargs:
            path = "members/{chamber}/{state}/{district}/current.json".format(**kwargs)

        elif 'state' in kwargs:
            path = "members/{chamber}/{state}/current.json".format(**kwargs)

        else:
            path = "{congress}/{chamber}/members.json".format(**kwargs)

        return self.fetch(path)
    
    def bills(self, member_id, type='introduced'):
        "Same as BillsClient.by_member"
        path = "members/{0}/bills/{1}.json".format(member_id, type)
        return self.fetch(path)
    
    def new(self, **kwargs):
        "Returns a list of new members"
        path = "members/new.json"
        return self.fetch(path)
    
    def departing(self, chamber, congress=CURRENT_CONGRESS):
        "Takes a chamber and congress and returns a list of departing members"
        check_chamber(chamber)
        path = "{0}/{1}/members/leaving.json".format(congress, chamber)
        return self.fetch(path)
    
    def compare(self, first, second, chamber, type='votes', congress=CURRENT_CONGRESS):
        """
        See how often two members voted together in a given Congress.
        Takes two member IDs, a chamber and a Congress number.
        """
        check_chamber(chamber)
        path = "members/{first}/{type}/{second}/{congress}/{chamber}.json"
        path = path.format(first=first, second=second, 
            type=type, congress=congress, chamber=chamber)
        return self.fetch(path)

    def party(self):
        "Get state party counts for the current Congress"
        path = "states/members/party.json"
        return self.fetch(path, parse=lambda r: r['results'])


class BillsClient(Client):
    
    def by_member(self, member_id, type='introduced'):
        """
        Takes a bioguide ID and a type (introduced|updated|cosponsored|withdrawn), 
        returns recent bills
        """
        path = "members/{member_id}/bills/{type}.json".format(member_id=member_id, type=type)
        return self.fetch(path)
    
    def get(self, bill_id, congress=CURRENT_CONGRESS, type=None):
        if type:
            path = "{congress}/bills/{bill_id}/{type}.json".format(
                congress=congress, bill_id=bill_id, type=type)
        else:
            path = "{congress}/bills/{bill_id}.json".format(
                congress=congress, bill_id=bill_id)

        return self.fetch(path)
    
    def amendments(self, bill_id, congress=CURRENT_CONGRESS):
        return self.get(bill_id, congress, 'amendments')

    def related(self, bill_id, congress=CURRENT_CONGRESS):
        return self.get(bill_id, congress, 'related')
    
    def subjects(self, bill_id, congress=CURRENT_CONGRESS):
        return self.get(bill_id, congress, 'subjects')
    
    def cosponsors(self, bill_id, congress=CURRENT_CONGRESS):
        return self.get(bill_id, congress, 'cosponsors')
    
    def recent(self, chamber, congress=CURRENT_CONGRESS, type='introduced'):
        check_chamber(chamber)
        "Takes a chamber, Congress, and type (introduced|updated), returns a list of recent bills"
        path = "{congress}/{chamber}/bills/{type}.json".format(
            congress=congress, chamber=chamber, type=type)
        return self.fetch(path)
    
    def introduced(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for getting introduced bills"
        return self.recent(chamber, congress, 'introduced')
    
    def updated(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for getting updated bills"
        return self.recent(chamber, congress, 'updated')

    def passed(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for passed bills"
        return self.recent(chamber, congress, 'passed')

    def major(self, chamber, congress=CURRENT_CONGRESS):
        "Shortcut for major bills"
        return self.recent(chamber, congress, 'major')


class VotesClient(Client):
    
    # date-based queries
    def by_month(self, chamber, year=None, month=None):
        """
        Return votes for a single month, defaulting to the current month.
        """
        check_chamber(chamber)

        now = datetime.datetime.now()
        year = year or now.year
        month = month or now.month
        
        path = "{chamber}/votes/{year}/{month}.json".format(
            chamber=chamber, year=year, month=month)
        return self.fetch(path, parse=lambda r: r['results'])
    
    def by_range(self, chamber, start, end):
        """
        Return votes cast in a chamber between two dates,
        up to one month apart.
        """
        check_chamber(chamber)

        start, end = parse_date(start), parse_date(end)
        if start > end:
            start, end = end, start

        path = "{chamber}/votes/{start:%Y-%m-%d}/{end:%Y-%m-%d}.json".format(
            chamber=chamber, start=start, end=end)
        return self.fetch(path, parse=lambda r: r['results'])
    
    def by_date(self, chamber, date):
        "Return votes cast in a chamber on a single day"
        date = parse_date(date)
        return self.by_range(chamber, date, date)
    
    def today(self, chamber):
        "Return today's votes in a given chamber"
        now = datetime.date.today()
        return self.by_range(chamber, now, now)
    
    # detail response
    def get(self, chamber, rollcall_num, session, congress=CURRENT_CONGRESS):
        "Return a specific roll-call vote, including a complete list of member positions"
        check_chamber(chamber)

        path = "{congress}/{chamber}/sessions/{session}/votes/{rollcall_num}.json"
        path = path.format(congress=congress, chamber=chamber, 
            session=session, rollcall_num=rollcall_num)
        return self.fetch(path, parse=lambda r: r['results'])
    
    # votes by type
    def by_type(self, chamber, type, congress=CURRENT_CONGRESS):
        "Return votes by type: missed, party, lone no, perfect"
        check_chamber(chamber)

        path = "{congress}/{chamber}/votes/{type}.json".format(
            congress=congress, chamber=chamber, type=type)
        return self.fetch(path)
    
    def missed(self, chamber, congress=CURRENT_CONGRESS):
        "Missed votes by member"
        return self.by_type(chamber, 'missed', congress)
    
    def party(self, chamber, congress=CURRENT_CONGRESS):
        "How often does each member vote with their party?"
        return self.by_type(chamber, 'party', congress)
    
    def loneno(self, chamber, congress=CURRENT_CONGRESS):
        "How often is each member the lone no vote?"
        return self.by_type(chamber, 'loneno', congress)
    
    def perfect(self, chamber, congress=CURRENT_CONGRESS):
        "Who never misses a vote?"
        return self.by_type(chamber, 'perfect', congress)
    
    def nominations(self, congress=CURRENT_CONGRESS):
        "Return votes on nominations from a given Congress"
        path = "{congress}/nominations.json".format(congress=congress)
        return self.fetch(path)


class CommitteesClient(Client):
    
    def filter(self, chamber, congress=CURRENT_CONGRESS):
        check_chamber(chamber)
        path = "{congress}/{chamber}/committees.json".format(
            congress=congress, chamber=chamber)
        return self.fetch(path)
    
    def get(self, chamber, committee, congress=CURRENT_CONGRESS):
        check_chamber(chamber)
        path = "{congress}/{chamber}/committees/{committee}.json".format(
            congress=congress, chamber=chamber, committee=committee)
        return self.fetch(path)


class NominationsClient(Client):
    
    def filter(self, type, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/{type}.json".format(congress=congress, type=type)
        return self.fetch(path)
    
    def get(self, nominee, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/{nominee}.json".format(congress=congress, nominee=nominee)
        return self.fetch(path)
    
    def by_state(self, state, congress=CURRENT_CONGRESS):
        path = "{congress}/nominees/state/{state}.json".format(
            congress=congress, state=state)
        return self.fetch(path)


class Congress(Client):
    """
    Implements the public interface for the NYT Congress API
    
    Methods are namespaced by topic (though some have multiple access points).
    Everything returns decoded JSON, with fat trimmed.
    
    In addition, the top-level namespace is itself a client, which
    can be used to fetch generic resources, using the API URIs included
    in responses. This is here so you don't have to write separate
    functions that add on your API key and trim fat off responses.
    
    Create a new instance with your API key, or set an environment
    variable called NYT_CONGRESS_API_KEY.
    
    Congress uses httplib2, and caching is pluggable. By default,
    it uses httplib2.FileCache, in a directory called .cache, but it
    should also work with memcache or anything else that exposes the
    same interface as FileCache (per httplib2 docs).
    """
    
    def __init__(self, apikey=os.environ.get('PROPUBLICA_API_KEY'), cache='.cache'):
        super(Congress, self).__init__(apikey, cache)
        self.members = MembersClient(self.apikey, cache)
        self.bills = BillsClient(self.apikey, cache)
        self.committees = CommitteesClient(self.apikey, cache)
        self.votes = VotesClient(self.apikey, cache)
        self.nominations = NominationsClient(self.apikey, cache)


