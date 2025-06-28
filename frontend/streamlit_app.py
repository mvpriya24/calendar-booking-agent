import streamlit as st
import dateparser
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
from datetime import timedelta

def clean_input(user_input):
    cleaned = re.sub(r'\b(please|schedule|book|appointment|meeting)\b', '', user_input, flags=re.IGNORECASE)
    return cleaned.strip()

def parse_appointment_time(user_input):
    settings = {
        'PREFER_DATES_FROM': 'future',
        'RETURN_AS_TIMEZONE_AWARE': False,
        'DATE_ORDER': 'DMY'
    }
    appointment_time = dateparser.parse(user_input, settings=settings)

    if not appointment_time:
        match = re.search(r'at (\d{1,2}(?:am|pm)) (.+)', user_input, re.IGNORECASE)
        if match:
            new_input = f"{match.group(2)} at {match.group(1)}"
            appointment_time = dateparser.parse(new_input, settings=settings)

    return appointment_time

def authenticate_google():
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return creds

def add_event_to_calendar(summary, start_time, end_time):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

st.title("🗓️ Calendar Booking Chatbot")
st.write("Welcome! Please type your request to book an appointment.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Your message:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    cleaned_input = clean_input(user_input)
    appointment_time = parse_appointment_time(cleaned_input)

    if appointment_time:
        appointment_end_time = appointment_time + timedelta(hours=1)
        event_link = add_event_to_calendar('Booked Appointment', appointment_time, appointment_end_time)
        bot_response = f"✅ Your appointment has been booked for: {appointment_time.strftime('%A, %d %B %Y at %I:%M %p')} \n\n📅 [View in Calendar]({event_link})"
    else:
        bot_response = "❌ Sorry, I couldn't understand the date. Please try again with a clear format like 'June 5th at 3pm'."

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
