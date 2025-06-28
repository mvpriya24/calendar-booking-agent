import streamlit as st
import datetime
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set the Google API scope
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def add_event_to_calendar(summary, start_time, end_time):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

# Example usage in your chatbot
st.title("🗓️ Calendar Booking Chatbot with Google Calendar Integration")

user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip() != "":
        now = datetime.datetime.now()
        appointment_time = now.replace(hour=15, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        appointment_end_time = appointment_time + datetime.timedelta(hours=1)

        # Add event to Google Calendar
        event_link = add_event_to_calendar('Booked Appointment', appointment_time, appointment_end_time)

        st.success(f"✅ Your appointment has been booked for: {appointment_time.strftime('%A, %d %B %Y at %I:%M %p')}")
        st.markdown(f"[View your event here]({event_link})")
    else:
        st.write("⚠️ Please enter a message.")
