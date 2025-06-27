from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def check_availability(time_str):
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    # Check events in the next 10 events starting from now
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    for event in events:
        if 'dateTime' in event['start']:
            existing_event_time = event['start']['dateTime'][:-1]  # Remove 'Z' for comparison
            if existing_event_time == time_str:
                return False  # Slot is already booked

    return True  # Slot is available

def book_slot(time_str):
    service = get_calendar_service()

    # Convert string to datetime object
    start_time = datetime.datetime.fromisoformat(time_str)
    end_time = start_time + datetime.timedelta(hours=1)  # Assuming 1-hour appointment

    event = {
        'summary': 'Booked Appointment',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    return event.get('htmlLink')
