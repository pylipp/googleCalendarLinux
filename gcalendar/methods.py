#!/usr/bin/env python

import uuid
import logging

import maya

from .utils import convert_datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def create(service, calendarId='primary', event_id=None, summary="",
        location="", description="", start=None, end=None, attendees=None,
        enable_reminders=True):
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

    :param enable_reminders: If true (default), send email a day before the
        event and display a popup 10 minutes in advance.
    :type enable_reminders: bool
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
        }

    if enable_reminders:
        event['reminders'] = {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            }

    logger.info("Created event: {}".format(event))
    response = service.events().insert(calendarId=calendarId, body=event).execute()
    logger.info("Received response: {}".format(response))


def fetch_events(service, calendarId='primary', start=None, end=None):
    """
    Fetch events of the specified calendar between start and end date.

    :param calendarId: ID of the calendar to insert the event. Default: 'primary'
    :type calendarId: str

    :param start: start date of the query in format dd/mm/yyyy
    :type start: str

    :param end: end date of the query in format dd/mm/yyyy. By default, this is
        24 hours after the start date.
    :type end: str
    """

    if start is None:
        raise AttributeError("Please provide start date for query.")

    if end is None:
        end = start

    # include events of entire end day
    end = maya.parse(end).add(hours=24).iso8601()

    logger.info("Reading events")
    response = service.events().list(
            calendarId=calendarId, timeMin=convert_datetime(start),
            timeMax=end, singleEvents=True, orderBy='startTime').execute()

    events = response['items']
    logger.info("Nr. of events found: {}".format(len(events)))

    return events


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
