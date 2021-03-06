#!/usr/bin/env python

import os

import maya
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def convert_datetime(date, day_first=True, **timedeltas):
    """Create timestamp from datetime string. Optionally timedeltas can be
    passed, they will be added after parsing the date string.

    :param date: Date to create the timestamp from
    :type date: str

    :param day_first: Kwarg for maya.parse() to distinguish ambiguous dates
    :type day_first: bool

    :param timedeltas: Kwargs to pass to maya.MayaDT.add(), e.g. hours,
        minutes, seconds.
    :type timedeltas: float
    """

    date = maya.parse(date, day_first=day_first)

    if timedeltas:
        date = date.add(**timedeltas)

    return date.iso8601()


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = os.path.join('..', 'client_secret.json')
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def build_service():
    """Get credentials, authorize and build a service."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)
