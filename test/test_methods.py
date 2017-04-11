#!/usr/bin/env python

import unittest

import httplib2
from apiclient import discovery

from gcalendar import methods, main


class ServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        credentials = main.get_credentials()
        http = credentials.authorize(httplib2.Http())
        cls.service = discovery.build('calendar', 'v3', http=http)

class CreateTestCase(ServiceTestCase):
    def test_create_only(self):
        methods.create(self.service,
                summary="Test summary",
                location="here",
                description="Lorem ipsum sit dolor amet.",
                start="11/04/2017 08:00:00",
                end="11/04/2017 16:00:00",
                attendees=["foo@bar.com"]
                )
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
