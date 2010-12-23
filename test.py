#!/usr/bin/env python

import datetime
import json
import os
import time
import urllib
import urllib2
import unittest

from nytcongress import NytCongress, NytCongressError, NytNotFoundError, get_congress

API_KEY = os.environ['NYT_CONGRESS_API_KEY']

class APITest(unittest.TestCase):
    
    def check_response(self, result, url, parse=lambda r: r['results'][0]):
        
        response = json.load(urllib2.urlopen(url))
        
        if parse and callable(parse):
            response = parse(response)
        
        self.assertEqual(result, response)
    
    def setUp(self):
        self.congress = NytCongress(API_KEY)
        time.sleep(.5)
    
class MemberTest(APITest):

    def test_get_member(self):
        pelosi = self.congress.members.get('P000197')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/P000197.json?api-key=%s" % API_KEY
        self.check_response(pelosi, url)
    
    def test_filter_members(self):
        ca = self.congress.members.filter(chamber='house', state='CA', congress=111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/members.json?&state=ca&api-key=%s" % API_KEY
        self.check_response(ca, url)
    
    def test_new_members(self):
        new = self.congress.members.new()
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/new.json?api-key=%s" % API_KEY
        self.check_response(new, url)

    def test_departing_members(self):
        new = self.congress.members.departing(chamber='house', congress=111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/members/leaving.json?api-key=%s" % API_KEY
        self.check_response(new, url)

class BillTest(APITest):
    
    def test_recent_bills(self):
        latest = self.congress.bills.recent(chamber='house', congress=111, type='introduced')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/bills/introduced.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_introduced_shortcut(self):
        latest = self.congress.bills.introduced('house')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/bills/introduced.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_updated_shortcut(self):
        latest = self.congress.bills.updated('house')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/bills/updated.json?api-key=%s" % API_KEY
        self.check_response(latest, url)
    
    def test_bills_by_member(self):
        farr_bills = self.congress.bills.by_member('F000030', 'introduced')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/F000030/bills/introduced.json?api-key=%s" % API_KEY
        self.check_response(farr_bills, url)
        
    def test_bill_detail(self):
        hr1 = self.congress.bills.get('hr1', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1.json?api-key=%s" % API_KEY
        self.check_response(hr1, url)
    
    def test_bill_amendments(self):
        hr1 = self.congress.bills.amendments('hr1', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1/amendments.json?api-key=%s" % API_KEY
        self.check_response(hr1, url)
    
    def test_bill_subjects(self):
        hr1 = self.congress.bills.subjects('hr1', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1/subjects.json?api-key=%s" % API_KEY
        self.check_response(hr1, url)
    
    def test_related_bills(self):
        hr1 = self.congress.bills.related('hr1', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1/related.json?api-key=%s" % API_KEY
        self.check_response(hr1, url)
    
    def test_bill_cosponsors(self):
        hr1 = self.congress.bills.cosponsors('hr1', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1/cosponsors.json?api-key=%s" % API_KEY
        self.check_response(hr1, url)

class CommitteeTest(APITest):
    
    def test_committee_list(self):
        house = self.congress.committees.filter('house', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/committees.json?api-key=%s" % API_KEY
        self.check_response(house, url)
        
        senate = self.congress.committees.filter('senate', 111)
        url2 = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/senate/committees.json?api-key=%s" % API_KEY
        self.check_response(senate, url2)
    
    def test_committee_detail(self):
        hsba = self.congress.committees.get('house', 'hsba', 111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/house/committees/HSBA.json?api-key=%s" % API_KEY
        self.check_response(hsba, url)

class NominationTest(APITest):
	
	def test_nomination_list(self):
		received = self.congress.nominations.filter('received', 111)
		url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominees/received.json?api-key=%s" % API_KEY
		self.check_response(received, url)
		
		withdrawn = self.congress.nominations.filter('withdrawn', 111)
		url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominees/withdrawn.json?api-key=%s" % API_KEY
		self.check_response(withdrawn, url)

		confirmed = self.congress.nominations.filter('confirmed', 111)
		url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominees/confirmed.json?api-key=%s" % API_KEY
		self.check_response(confirmed, url)

		updated = self.congress.nominations.filter('updated', 111)
		url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominees/updated.json?api-key=%s" % API_KEY
		self.check_response(updated, url)
		
	def test_nomination_detail(self):
	    pn250 = self.congress.nominations.get('PN250', 111)
	    url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominees/PN250.json?api-key=%s" % API_KEY
	    self.check_response(pn250, url)


class VoteTest(APITest):
    
    def test_votes_by_month(self):
        jan = self.congress.votes.by_month('house', 2010, 1)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/house/votes/2010/01.json?api-key=%s" % API_KEY
        self.check_response(jan, url, parse=lambda r: r['results'])
    
    def test_votes_by_date_range(self):
        sept = self.congress.votes.by_range('house', datetime.date(2010, 9, 1), datetime.date(2010, 9, 30))
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/house/votes/2010-09-1/2010-09-30.json?api-key=%s" \
            % API_KEY
        self.check_response(sept, url, parse=lambda r: r['results'])
    
    def test_votes_by_reversed_range(self):
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        self.assertEqual(
            self.congress.votes.by_range('house', today, last_week),
            self.congress.votes.by_range('house', last_week, today)
        )
    
    def test_votes_today(self):
        today = datetime.datetime.today()
        votes = self.congress.votes.today('house')
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/" \
              "congress/house/votes/%(today)s/%(today)s.json?api-key=%(key)s" \
                  % {'today': today.strftime('%Y-%m-%d'), 'key': API_KEY}
        self.check_response(votes, url, parse=lambda r: r['results'])
    
    def test_votes_by_date(self):
        june14 = datetime.date(2010, 6, 14)
        votes = self.congress.votes.by_date('house', june14)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "house/votes/2010-06-14/2010-06-14.json?api-key=%s" % API_KEY)
        self.check_response(votes, url, parse=lambda r: r['results'])
    
    def test_vote_rollcall(self):
        vote = self.congress.votes.get('house', 580, 2, 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/sessions/2/votes/580.json?api-key=%s" % API_KEY)
        self.check_response(vote, url, parse=lambda r: r['results'])
    
    def test_votes_by_type(self):
        missed = self.congress.votes.by_type('house', 'missed', 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/votes/missed.json?api-key=%s" % API_KEY)
        self.check_response(missed, url)
    
    def test_missed_votes(self):
        missed = self.congress.votes.missed('house', 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/votes/missed.json?api-key=%s" % API_KEY)
        self.check_response(missed, url)
    
    def test_party_votes(self):
        party = self.congress.votes.party('house', 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/votes/party.json?api-key=%s" % API_KEY)
        self.check_response(party, url)
    
    def test_loneno_votes(self):
        lonenos = self.congress.votes.loneno('house', 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/votes/loneno.json?api-key=%s" % API_KEY)
        self.check_response(lonenos, url)
    
    def test_perfect_voters(self):
        perfects = self.congress.votes.perfect('house', 111)
        url = ("http://api.nytimes.com/svc/politics/v3/us/legislative/congress/"
               "111/house/votes/perfect.json?api-key=%s" % API_KEY)
        self.check_response(perfects, url)
    
    def test_nominations(self):
        nom_votes = self.congress.votes.nominations(111)
        url = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/nominations.json?api-key=%s" % API_KEY
        self.check_response(nom_votes, url)
    
class ClientTest(APITest):

    def test_generic_fetch(self):
        hr1 = self.congress.bills.get('hr1', 111)
        hr1_generic = self.congress.fetch('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1.json')
        self.assertEqual(hr1, hr1_generic)

class ErrorTest(APITest):
    
    def test_bad_vote_args(self):
        # this needs a chamber argument
        self.assertRaises(TypeError, self.congress.votes.by_month, 2010, 11)
    
    def test_no_chamber_args(self):
        # this takes a chamber argument, not a member_id
        self.assertRaises(NytCongressError, self.congress.bills.introduced, 'N000032')
    
    def test_404(self):
        # the API returns a 404 for members not found
        self.assertRaises(NytNotFoundError, self.congress.members.get, 'notamember')

class UtilTest(unittest.TestCase):

    def test_congress_years(self):
        
        self.assertEqual(get_congress(1809), 11)
        self.assertEqual(get_congress(1810), 11)
        self.assertEqual(get_congress(2009), 111)
        self.assertEqual(get_congress(2010), 111)

class DjangoTest(unittest.TestCase):
    
    def test_django_cache(self):
        try:
            from django.conf import settings
            settings.configure(CACHE_BACKEND = 'locmem://')
            from django.core.cache import cache
        except ImportError:
            # no Django, so nothing to test
            return
        
        congress = NytCongress(API_KEY, cache)
        
        self.assertEqual(congress.http.cache, cache)
        self.assertEqual(congress.members.http.cache, cache)
        self.assertEqual(congress.bills.http.cache, cache)
        self.assertEqual(congress.votes.http.cache, cache)
        
        try:
            bills = congress.bills.introduced('house')
        except Exception, e:
            self.fail(e)
        

if __name__ == "__main__":
    unittest.main()
