#!/usr/bin/env python

import unittest
import uuid

from apiclient import http

from gcalendar import methods, utils


class ServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = utils.build_service()

    def test_create_seek_and_destroy(self):
        summary = "Test summary"
        event_id = uuid.uuid4().hex
        start = "11/04/2017"
        methods.create(self.service,
                event_id=event_id,
                summary=summary,
                location="here",
                description="Lorem ipsum sit dolor amet.",
                start="{} 08:00:00".format(start),
                end="{} 16:00:00".format(start),
                attendees=["foo@bar.com"]
                )
        events = methods.fetch_events(self.service,
                start=start)
        nr_events = len(events)

        self.assertGreaterEqual(nr_events, 1)
        self.assertIn(summary, [event["summary"] for event in events])

        methods.delete_event(self.service, event_id)
        events = methods.fetch_events(self.service, start=start)
        self.assertEqual(len(events) + 1, nr_events)

    def test_list(self):
        calendars = dict(methods.list(self.service))
        # assuming the calendar list contains at least the 'Week numbers'
        self.assertGreaterEqual(len(calendars), 1)
        self.assertIn("Week Numbers", calendars.keys())

    def test_delete_nonexisting_event(self):
        event_id = uuid.uuid4().hex
        self.assertRaises(http.HttpError, methods.delete_event, self.service, event_id)

    def test_create_event_body_kwargs(self):
        summary = "Event with source link to GitHub"
        start = "16/04/2017"
        event_id = uuid.uuid4().hex
        methods.create(self.service,
                event_id=event_id,
                summary=summary,
                start="{} 08:00:00".format(start),
                end="{} 16:00:00".format(start),
                source={
                    "url": "https://github.com/pylipp/googleCalendarLinux",
                    "title": "Python package to interact with Google Calendar"
                    }
                )

        events = methods.fetch_events(self.service, start=start)
        self.assertIn(summary, [event["summary"] for event in events])

        methods.delete_event(self.service, event_id)

    def test_create_without_event_id(self):
        start = "16/04/2017"
        event_id = methods.create(self.service,
                start="{} 08:00:00".format(start),
                end="{} 16:00:00".format(start)
                )

        methods.delete_event(self.service, event_id)

if __name__ == "__main__":
    unittest.main()
