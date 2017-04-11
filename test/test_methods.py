#!/usr/bin/env python

import unittest

from gcalendar import methods, utils


class ServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = utils.build_service()

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
