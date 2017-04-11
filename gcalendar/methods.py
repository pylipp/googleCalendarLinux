#!/usr/bin/env python

import uuid
import logging

import maya


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def create(service, calendarId='primary', event_id=None, summary="",
        location="", description="", start=None, end=None, attendees=None):
    """
    Create an event request object and insert it in the calendar's events.

    :param calendarId: ID of the calendar to insert the event. Default: 'primary'
    :type calendarId: str

    :param event_id: unique ID to identify the event. By default, a UUID is created
    :type event_id: str

    :param start: event starting datetime in format dd/mm/yyyy hh:mm:ss.
    :type start: str
    :param end: event ending datetime in format dd/mm/yyyy hh:mm:ss.
    :type end: str

    :param attendees: list of attendees' emails
    :type attendees: list[str]
    """

    if not all([summary, location, description, start, end, attendees]):
        raise AttributeError("Missing mandatory argument")

    if event_id is None:
        event_id = uuid.uuid4().hex

    datetime_start = _convert_datetime(start)
    datetime_end = _convert_datetime(end)

    attendee_emails = [{"email": mail} for mail in attendees]

    event = {
        'id': event_id,
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
          'dateTime': datetime_start,
        },
        'end': {
          'dateTime': datetime_end,
        },
        'attendees': attendee_emails,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
        },
    }

    logger.info("Created event: {}".format(event))
    response = service.events().insert(calendarId=calendarId, body=event).execute()
    logger.info("Received response: {}".format(response))


DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

def _convert_datetime(date, day_first=True):
    """Create timestamp from datetime string."""
    date = maya.parse(date, day_first=day_first)
    return date.iso8601()
