#!/usr/bin/env python
from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from time import timezone
from math import fabs

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
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


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    while 1:		#Menu Driven program to allow user to execute the required function
        try:
            print('\n', '-'*50)
            choice = int(input('What would you like to do?\n\t1. Read Events\t\t2. Get Details of an Event\n\t3. Create Event\t\t4. Delete Event\n\t5. Edit Events\t\t6. Exit\nYour Choice: '))
        except ValueError:
            choice = 7

        if choice == 1:
            read(service)
        elif choice == 2:
            elaborate(service)
        elif choice == 3:
            create(service)
        elif choice == 4:
            delevent(service)
        elif choice == 5:
            edit(service)
        elif choice == 6:
            print('\nExiting. Have a nice day!')
            sys.exit()
        else:
             print('Kindly enter a valid number between 1-6.')


def read(service):
    #Allows user to see all the events on the given day in calendar
    try:
        start_date = datetime.datetime.strptime(input('\nDate to read from (dd/mm/yyyy): '), "%d/%m/%Y")         #Inputting the date for which calendar has to be accessed
        finish_date = datetime.datetime.strptime(input('Date to read till (dd/mm/yyyy): '), "%d/%m/%Y")         #Inputting the date for which calendar has to be accessed
        finish_date = finish_date + datetime.timedelta(1,0,0)
    except ValueError:
        print('Illegal Date Format. Kindly enter the date in dd/mm/yyyy format.')
        return
    
    eventsResult = service.events().list(
        calendarId='primary', timeMin=start_date.isoformat()+'Z', timeMax=finish_date.isoformat()+'Z', singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        print('')
        print(events.__len__(), ' events found.')

    for event in events:
        print('\tID:', event['id'], '  ---  ', 'Title:', event['summary'])

def elaborate(service):
    #Allows user to see details of a particular event in the calendar. Specially modified for the attendees field of an event
    eventId = input('\nEnter required event\'s ID: ')
    try:
    	event = service.events().get(calendarId='primary', eventId=eventId).execute()
    except:
    	print('Invalid ID. Please try again.')
    	return
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    print (event['summary'], 'from', start.split('T')[0], ',', start.split('T')[1].split('+')[0], 'till', end.split('T')[0], ', ',  end.split('T')[1].split('+')[0])
    while 1:
        param = input('\nWhich other detail would you like to see? (Enter "all" to see all, "none" to exit): ')
        param = param.lower()
        if param == 'none':
            return
        elif param == 'all':
        	for par in event:
        		print(par, ':', event[par])
        elif param == 'attendees':
        	for att in event[param]:
        		print(att['email'])
        elif param == 'start':
            print ('start:', start.split('T')[0], ',', start.split('T')[1].split('+')[0])
        elif param == 'end':
            print('end:', end.split('T')[0], ', ',  end.split('T')[1].split('+')[0])
        elif param in ['organizer', 'creator']:
            print (param, ':', event[param]['displayName'])
        elif param in event.keys():
        	print (param, ':', event[param])
        else:
        	print('No such detail exists. Please enter valid parameters of the \'event\' object. eg: description, location, attendees, visibility, colorId, recurrence etc.')


def edit(service):
    #Allows user to edit details of a particular event in the calendar. Specially modified for the attendees, start and end fields of an event
    eventId = input('\nEnter ID of event to be edited: ')
    try:
    	event = service.events().get(calendarId='primary', eventId=eventId).execute()
    except:
    	print('Invalid ID. Please try again.')
    	return

    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    print (event['summary'], 'from', start.split('T')[0], ',', start.split('T')[1].split('+')[0], 'till', end.split('T')[0], ', ',  end.split('T')[1].split('+')[0])
    
    master = 1
    while master == 1:
        param = input('\nWhich detail would you like to modify? (Enter "see" to see all current details, "none" to exit): ')
        param = param.lower()
        if param == 'none':
        	master = 0
        
        elif param == 'see':
        	for par in event:
        		print(par, ':', event[par])
        
        elif param == 'start':
        	offset = timezone*(+1)
        	start = datetime.datetime.strptime(input('Enter new Start date & time (dd/mm/yyyy hh:mm:ss): '), "%d/%m/%Y %H:%M:%S")
        	start = start + datetime.timedelta(0,offset,0)
        	startDateTime = str(start.date())+'T'+str(start.time())+'Z'
        	event[param]['dateTime'] = startDateTime
        
        elif param == 'end':
        	offset = timezone*(+1)
        	end = datetime.datetime.strptime(input('Enter new End date & time (dd/mm/yyyy hh:mm:ss): '), "%d/%m/%Y %H:%M:%S")
        	end = end + datetime.timedelta(0,offset,0)
        	endDateTime = str(end.date())+'T'+str(end.time())+'Z'
        	event[param]['dateTime'] = endDateTime
        
        elif param == 'id':
            print('Sorry! ID of an event can not be modified!')
            continue

        elif param == 'attendees':
        	if param not in event.keys():
        		event[param] = []
        	choice = input('Enter 1 to ADD an Attendee, 0 to REMOVE an Attendee: ')
        	if choice == '1':
        		dispName = input('\tEnter Name of Attendee: ')
        		mail = input('\tEnter email of Attendee: ')
        		event[param].append({'displayName':dispName, 'email':mail})
        	elif choice == '0':
        		mail = input('\tEnter email of the attendee to be removed: ')
        		flag = 0                #setting flag to 0
        		for att in event[param]:
        			if att['email'] == mail:
        				event[param].remove(att)
        				print('Attendee removed.')
        				flag = 1        #attendee found, setting flag to 1
        		if flag == 0:           #flag is 0 if attendee is not found
        			print('Attendee not found.')
        	else:
        		print('Invalid Input. Kindly enter 0 or 1.')
        
        else:
            if param not in event.keys():
            	event[param] = ''
            event[param] = input('Enter value to be stored with this parameter: ')
        
        try:
            event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            if param not in ['see', 'none']:
                print('Event Modified!')
        except:
          	print ('Please check the parameter and value entered. Ensure valid parameters of the \'event\' object are entered. eg: description, location, attendees, visibility, colorId, recurrence etc. Also ensure value entered for the parameter is typesafe.')

def create(service):
	#Allows users to create new event. Specially modified for start/end date-times, number of attendees, title, location, id and description
    print('\nEnter details for the new event.')
    e_id = input('\nID (length between 5-1024 using lowercase a-v & 0-9): ')
    for char in e_id:
        if not (char.isdigit() or (ord(char)>=97 and ord(char)<=118)):
            print('Event ID entered is illegal. Please enter characters between lowercase a-v or digits 0-9. Also, length of ID must be between 5-1024.')
            return
    
    summary = input('Title: ')
    location = input('Location: ')
    description = input('Description: ')

    offset = timezone
    
    start = datetime.datetime.strptime(input('Start Date & Time (dd/mm/yyyy hh:mm:ss): '), "%d/%m/%Y %H:%M:%S")
    start = start + datetime.timedelta(0,offset,0)
    startDateTime = str(start.date())+'T'+str(start.time())+'Z'

    end = datetime.datetime.strptime(input('End Date & Time (dd/mm/yyyy hh:mm:ss): '), "%d/%m/%Y %H:%M:%S")
    end = end + datetime.timedelta(0,offset,0)
    endDateTime = str(end.date())+'T'+str(end.time())+'Z'

    try:
        att = int(input('Enter Number of Attendees: '))
    except ValueError:
        print('Please enter a valid number.')
        return

    attendees = []
    for i in range(0, att):
        attendees.append({'email':input('Enter email of Attendee #'+str(i+1)+': ')})
    
    event = {
        'id': e_id,
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
          'dateTime': startDateTime,
        },
        'end': {
          'dateTime': endDateTime,
        },
        'attendees': attendees,
        'reminders': {
          'useDefault': False,
          'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
          ],
        },
    }
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event has been added!')
    except:
        print(event)

def delevent(service):
	#Allows user to delete an event according to event ID
    eventId = input('Enter ID of the event to be deleted: ')
    try:
    	service.events().delete(calendarId='primary', eventId=eventId).execute()
    	print('\nEvent deleted!')
    except:
        print('\nInvalid event ID!')

if __name__ == '__main__':
    main()