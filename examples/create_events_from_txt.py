#!/usr/bin/env python
"""
Example script that reads in working day and hours from a file and creates the
respective events. Useful if your working hours are tracked on GoogleCalendar.
Events that are already present will be updated.
"""

import os
from datetime import datetime
from collections import namedtuple

import maya

from gcalendar import methods, utils


script_dir = os.path.dirname(os.path.abspath(__file__))

WorkDay = namedtuple("WorkDay", ["start", "end"])

workdays = []
with open(os.path.join(script_dir, "2017_working_hours.txt")) as f:
    for line in f:
        if line.startswith("#"):
            continue

        try:
            date, hours = line.strip().split()
            # start the day at 9am
            start = maya.parse(date).add(hours=9)
            end = start.add(hours=float(hours))
            workday = WorkDay(
                    start.datetime().strftime("%d/%m/%Y %H:%M:%S"),
                    end.datetime().strftime("%d/%m/%Y %H:%M:%S")
                    )
            workdays.append(workday)
        except Exception as e:
            print("Parsing error: {}".format(e))
            print("Skipping line: {}".format(line))
            continue

service = utils.build_service()
calendarId = dict(methods.list(service))["MUC working students attendance"]

for workday in workdays:
    events = methods.fetch_events(service,
            calendarId=calendarId,
            start=workday.start.split()[0]
            )
    summary = "Philipp Metzner"

    existing_event = None
    for event in events:
        if event["summary"] == summary:
            existing_event = event
            break
    if existing_event is not None:
        print("Event already exists, is being updated!")
        methods.delete_event(service, existing_event["id"],
                calendarId=calendarId)

    methods.create(service,
            calendarId=calendarId,
            summary=summary,
            start=workday.start,
            end=workday.end
            )
