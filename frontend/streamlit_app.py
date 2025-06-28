from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# After authentication setup (requires OAuth token flow)
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])

service = build('calendar', 'v3', credentials=creds)

event = {
  'summary': 'Booked Appointment',
  'start': {'dateTime': '2024-07-05T14:00:00', 'timeZone': 'Asia/Kolkata'},
  'end': {'dateTime': '2024-07-05T15:00:00', 'timeZone': 'Asia/Kolkata'},
}

event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: %s' % (event.get('htmlLink')))
