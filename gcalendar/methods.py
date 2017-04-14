#!/usr/bin/env python

"""Wrappers around the Google Calendar API to interact with events and
calendars."""

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
        enable_reminders=True, **body_kwargs):
    """
    Create an event request object and insert it in the calendar's events.

    :param calendarId: ID of the calendar to insert the event. Default: 'primary'
    :type calendarId: str

    :param event_id: unique ID to identify the event. Created by Google if omitted
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

    :param body_kwargs: Its contents are added to the event body. This allows
        for adding custom fields acc. to the specification, e.g. recurrence.
        This will also overwrite fields that are redefined.
        (https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#insert)

    :raises AttributeError: if any argument of summary, start or end is unspecified
    :raises Errors are propagated from the apiclient module.

    :returns event_id: ID of the created event, if successful
    :type event_id: str
    """

    if not all([start, end]):
        raise AttributeError("Missing mandatory argument")

    datetime_start = convert_datetime(start)
    datetime_end = convert_datetime(end)

    attendee_emails = [] if attendees is None else [{"email": mail} for mail in attendees]

    event = {
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

    if event_id is not None:
        event['id'] = event_id

    if enable_reminders:
        event['reminders'] = {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            }

    event.update(body_kwargs)

    logger.info("About to create event")
    response = service.events().insert(calendarId=calendarId, body=event).execute()
    event_id = response["id"]
    logger.info("Successfully created event with ID={}".format(event_id))

    return event_id


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

    :returns list[dict]
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


def delete_event(service, event_id, calendarId='primary'):
    """
    Delete event specified by ID from calendar.

    :param event_id: ID of the event to be deleted
    :type event_id: str

    :param calendarId: ID of the calendar to insert the event. Default: 'primary'
    :type calendarId: str

    :raises Errors are propagated from the apiclient module (e.g. HTTPError if
        the event_id is not found.)
    """

    logger.info("About to delete event with ID={}".format(event_id))
    service.events().delete(calendarId=calendarId, eventId=event_id).execute()
    logger.info("Successfully deleted event")


def list(service):
    """
    Generator function yielding a (summary, ID) tuple for every calendar.

    Convenient to find out the human-readable name (summary) and the ID of the
    calendar.

    :yields tuple(str, str)
    """

    response = service.calendarList().list().execute()
    logger.info("Received response: {}".format(response))

    for item in response["items"]:
        yield item["summary"], item["id"]
