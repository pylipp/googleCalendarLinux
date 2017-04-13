#!/usr/bin/env python
from __future__ import print_function
import sys

import datetime
from time import timezone
from math import fabs

from gcalendar import methods, utils


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    service = utils.build_service()

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
        start_date = input('\nDate to read from (dd/mm/yyyy): ')
        finish_date = input('Date to read till (dd/mm/yyyy): ')
    except ValueError:
        print('Illegal Date Format. Kindly enter the date in dd/mm/yyyy format.')
        return

    events = methods.fetch_events(service,
            start=start_date,
            end=finish_date
            )

    if not events:
        print('No upcoming events found.')
    else:
        print('')
        print(len(events), 'events found.')

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
            print('Event ID entered is illegal. A random UUID will be generated.')
            e_id = None

    summary = input('Title: ')
    location = input('Location: ')
    description = input('Description: ')

    start = input('Start Date & Time (dd/mm/yyyy hh:mm:ss): ')
    end = input('End Date & Time (dd/mm/yyyy hh:mm:ss): ')

    try:
        att = int(input('Enter Number of Attendees: '))
    except ValueError:
        print('Please enter a valid number.')
        return

    attendees = []
    for i in range(0, att):
        attendees.append(input('Enter email of Attendee #'+str(i+1)+': '))

    try:
        methods.create(service, event_id=e_id, summary=summary,
                location=location, description=description, start=start,
                end=end, attendees=attendees)
        print('Event has been added!')
    except AttributeError:
        raise
    except Exception as e:
        print("Error creating event: {}".format(e))

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
