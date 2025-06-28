import streamlit as st
import requests
import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import dateparser

# Streamlit UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #74ebd5, #ACB6E5);
        background-attachment: fixed;
        color: #333333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗓️ Calendar Booking Chatbot")
st.write("Welcome! Please type your request to book an appointment.")

# Authenticate Google
def authenticate_google():
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/calendar"])
    return creds

# Add event to Google Calendar
def add_event_to_calendar(summary, start_time, end_time):
    creds = authenticate_google()
    service = build("calendar", "v3", credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    calendar_id = 'primary'
    event_result = service.events().insert(calendarId=calendar_id, body=event).execute()

    return event_result.get('htmlLink')

# Input processing
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip() != "":
        parsed_date = dateparser.parse(user_input, settings={'PREFER_DATES_FROM': 'future'})
        if parsed_date:
            appointment_time = parsed_date
            appointment_end_time = appointment_time + datetime.timedelta(hours=1)

            try:
                event_link = add_event_to_calendar('Booked Appointment', appointment_time, appointment_end_time)
                st.write(f"✅ Your appointment has been booked for: {appointment_time.strftime('%A, %d %B %Y at %I:%M %p')}")
                st.write(f"📅 [View your event here]({event_link})")
            except Exception as e:
                st.write("⚠️ Google Calendar Error:", str(e))
        else:
            st.write("❌ Sorry, I couldn't understand the date. Please try again with more details.")
    else:
        st.write("Please enter a message to book an appointment.")
