import streamlit as st
import dateparser
from datetime import datetime

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip() != "":
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Parse the date from user input
        parsed_date = dateparser.parse(user_input, settings={'PREFER_DATES_FROM': 'future'})

        if parsed_date:
            if parsed_date > datetime.now():
                formatted_date = parsed_date.strftime('%A, %d %B %Y at %I:%M %p')
                bot_response = f"✅ Your appointment has been booked for: {formatted_date}"
            else:
                bot_response = "❌ Please provide a future date and time."
        else:
            bot_response = "❌ Sorry, I couldn't understand the date. Please try again with more details."

        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    else:
        st.write("⚠️ Please enter a message.")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"🧑 You: {message['content']}")
    else:
        st.write(f"🤖 Bot: {message['content']}")
