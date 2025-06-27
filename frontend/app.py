import streamlit as st
import requests

st.set_page_config(page_title="Calendar Booking Chatbot")

st.title("🗓️ Calendar Booking Chatbot")
st.write("Welcome! Please type your request to book an appointment.")

# Chat input
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
            if response.status_code == 200:
                bot_reply = response.json().get("response")
                st.success(bot_reply)
            else:
                st.error("⚠️ Error: " + str(response.status_code))
        except Exception as e:
            st.error(f"⚠️ Exception occurred: {e}")
    else:
        st.warning("Please type a message.")
