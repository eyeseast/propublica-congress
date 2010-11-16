#!/usr/bin/env python

import json
import os
import time
import urllib
import urllib2
import unittest

from nytcongress import NytCongress, get_congress

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

class ClientTest(APITest):

    def test_generic_fetch(self):
        hr1 = self.congress.bills.get('hr1', 111)
        hr1_generic = self.congress.fetch('http://api.nytimes.com/svc/politics/v3/us/legislative/congress/111/bills/hr1.json')
        self.assertEqual(hr1, hr1_generic)

class UtilTest(unittest.TestCase):

    def test_congress_years(self):
        
        self.assertEqual(get_congress(1809), 11)
        self.assertEqual(get_congress(1810), 11)
        self.assertEqual(get_congress(2009), 111)
        self.assertEqual(get_congress(2010), 111)


if __name__ == "__main__":
    unittest.main()