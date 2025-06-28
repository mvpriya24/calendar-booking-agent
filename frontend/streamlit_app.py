import streamlit as st
from datetime import timedelta
import dateparser.search
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Add pastel color gradient background
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fbd3e9, #bbded6, #e0c3fc);
        background-attachment: fixed;
        background-size: cover;
        color: #333333;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .stTextInput>div>div>input {
        background-color: white;
        color: black;
    }
    .stButton>button {
        background-color: #ffb6b9;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #f67280;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖🗓️ Calendar Booking Chatbot")
st.write("Welcome! Please type your request to book an appointment.")

# Load Google Credentials from Streamlit secrets
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])

def authenticate_google():
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

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result.get('htmlLink', 'No link available')

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip() != "":
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Search for date in the sentence
        result = dateparser.search.search_dates(user_input, settings={'PREFER_DATES_FROM': 'future'})

        if result:
            appointment_time = result[0][1]  # Take the first detected date
            appointment_end_time = appointment_time + timedelta(hours=1)
            event_link = add_event_to_calendar('Booked Appointment', appointment_time, appointment_end_time)
            bot_response = f"✅ Your appointment has been booked for: {appointment_time.strftime('%A, %d %B %Y at %I:%M %p')}\n[View in Google Calendar]({event_link})"
        else:
            bot_response = "❌ Sorry, I couldn't understand the date. Please try again with a clear format like 'July 5th at 3pm'."

        st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
