import streamlit as st
from datetime import datetime, timedelta
import re

# Beautiful background style
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

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Your message:")

def parse_time(time_str):
    """Try multiple time formats and return a datetime.time object."""
    formats = ["%I%p", "%I:%M%p", "%H:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except:
            continue
    return None

def simple_parser(message):
    message = message.lower()
    now = datetime.now()

    # Detect if "tomorrow" is in message
    if "tomorrow" in message:
        if "at" in message:
            try:
                time_part = message.split("at")[1].strip()
                time_obj = parse_time(time_part)
                if time_obj:
                    appointment_date = now + timedelta(days=1)
                    final_datetime = appointment_date.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                    return final_datetime
            except:
                return None

    # If no "tomorrow", assume tomorrow by default if time is mentioned
    if "at" in message:
        try:
            time_part = message.split("at")[1].strip()
            time_obj = parse_time(time_part)
            if time_obj:
                appointment_date = now + timedelta(days=1)
                final_datetime = appointment_date.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                return final_datetime
        except:
            return None

    return None

if st.button("Send"):
    if user_input.strip() != "":
        st.session_state.messages.append({"role": "user", "content": user_input})

        parsed_date = simple_parser(user_input)

        if parsed_date:
            if parsed_date > datetime.now():
                formatted_date = parsed_date.strftime('%A, %d %B %Y at %I:%M %p')
                bot_response = f"✅ Your appointment has been booked for: {formatted_date}"
            else:
                bot_response = "❌ Please provide a future date and time."
        else:
            bot_response = "❌ Sorry, I couldn't understand the date. Please use formats like 'tomorrow at 3pm', 'at 14:00', or 'at 4:30pm'."

        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    else:
        st.write("⚠️ Please enter a message.")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"🧑 You: {message['content']}")
    else:
        st.write(f"🤖 Bot: {message['content']}")
