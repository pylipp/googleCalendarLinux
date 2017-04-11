#!/usr/bin/env python

import uuid
import logging

from .utils import convert_datetime

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

    if not all([summary, start, end]):
        raise AttributeError("Missing mandatory argument")

    if event_id is None:
        event_id = uuid.uuid4().hex

    datetime_start = convert_datetime(start)
    datetime_end = convert_datetime(end)

    attendee_emails = [] if attendees is None else [{"email": mail} for mail in attendees]

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


def list(service):
    """
    Generator function yielding a (summary, ID) tuple for every calendar.

    Convenient to find out the human-readable name (summary) and the ID of the
    calendar.
    """

    response = service.calendarList().list().execute()
    logger.info("Received response: {}".format(response))

    for item in response["items"]:
        yield item["summary"], item["id"]
