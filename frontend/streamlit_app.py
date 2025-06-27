import streamlit as st
import requests

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

user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip() != "":
        try:
            # Correct backend port
            response = requests.post("http://127.0.0.1:8001/chat", json={"message": user_input})
            if response.status_code == 200:
                bot_response = response.json().get("response", "No response from bot.")
                st.write("🤖 Bot:", bot_response)
            else:
                st.write("⚠️ Error:", response.status_code)
        except Exception as e:
            st.write("⚠️ Exception:", str(e))
    else:
        st.write("Please enter a message.")
