#!/usr/bin/env python

import unittest

from gcalendar import methods, utils


class ServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = utils.build_service()

    def test_create_only(self):
        summary = "Test summary"
        methods.create(self.service,
                summary=summary,
                location="here",
                description="Lorem ipsum sit dolor amet.",
                start="11/04/2017 08:00:00",
                end="11/04/2017 16:00:00",
                attendees=["foo@bar.com"]
                )
        events = methods.fetch_events(self.service,
                start="11/04/2017")

        self.assertGreaterEqual(len(events), 1)
        self.assertIn(summary, [event["summary"] for event in events])

    def test_list(self):
        calendars = dict(methods.list(self.service))
        # assuming the calendar list contains at least the 'Week numbers'
        self.assertGreaterEqual(len(calendars), 1)
        self.assertIn("Week Numbers", calendars.keys())


if __name__ == "__main__":
    unittest.main()
