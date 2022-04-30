from __future__ import print_function
from calendar import calendar

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/calendar.events"]

class Calender:
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    @classmethod
    def get_all_events(cls):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(calendarId='s2750gl9659ocqi4if3fndqa7k@group.calendar.google.com', singleEvents=True).execute()
            all_events = events_result.get('items')

            if not all_events:
                print('No upcoming events found.')
                return False

            return all_events

        except HttpError as error:
            print('An error occurred: %s' % error)


    @classmethod
    def get_weekly_events(cls):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 7 events')
            print(now)
            events_result = service.events().list(calendarId='s2750gl9659ocqi4if3fndqa7k@group.calendar.google.com', timeMin=now,
                                                  maxResults=7, singleEvents=True,
                                                  orderBy='startTime').execute()
            weekly_events = events_result.get('items')

            if not weekly_events:
                print('No upcoming events found.')
                return False

            return weekly_events

        except HttpError as error:
            print('An error occurred: %s' % error)

    @classmethod
    def addevents(cls, data:dict) -> object:
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            
            event = {
            'summary': data['name'],
            'location': data['location'],
            'description': data['description'],
            'start': {
                'date': data['date'],
            },
            'end': {
                'date': data['date']
            }
            }
            print(event)
            service.events().insert(calendarId='s2750gl9659ocqi4if3fndqa7k@group.calendar.google.com', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            return event.get('id')

        except HttpError as error:
            print('An error occurred: %s' % error)


    @classmethod
    def delete_event(cls, id:int) -> int:
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            service.events().delete(calendarId='s2750gl9659ocqi4if3fndqa7k@group.calendar.google.com', eventId=id).execute()

            print('Event Deleted')

        except HttpError as error:
            print('An error occurred: %s' % error)
