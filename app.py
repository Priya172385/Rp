import streamlit as st
import pandas as pd
import smtplib
import time
import threading
from datetime import datetime
from email.message import EmailMessage

# --- CONFIGURATION ---
# Replace these with your actual details
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # Use a Google App Password here
RECEIVER_EMAIL = "receiver_email@gmail.com"

# --- EMAIL FUNCTION ---
def send_email(medicine_name, dose):
    msg = EmailMessage()
    msg.set_content(f"Time to take your medicine: {medicine_name} ({dose}).")
    msg['Subject'] = f"Medicine Reminder: {medicine_name}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- BACKGROUND SCHEDULER ---
def check_schedule():
    while True:
        now = datetime.now().strftime("%I:%M %p") # 12-hour format (e.g., 08:30 PM)
        if "schedule" in st.session_state:
            for index, row in st.session_state.schedule.iterrows():
                if row['Time'] == now and not row['Sent']:
                    success = send_email(row['Medicine'], row['Dose'])
                    if success:
                        st.session_state.schedule.at[index, 'Sent'] = True
        time.sleep(60) # Check every minute

# --- STREAMLIT UI ---
st.title("💊 Smart Medicine Reminder")

if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame(columns=["Medicine", "Dose", "Time", "Sent"])

# Start background thread once
if "thread_started" not in st.session_state:
    thread = threading.Thread(target=check_schedule, daemon=True)
    thread.start()
    st.session_state.thread_started = True

with st.form("med_form", clear_on_submit=True):
    name = st.text_input("Medicine Name")
    dose = st.text_input("Dosage (e.g., 1 tablet)")
    # Time picker converts to string AM/PM
    med_time = st.time_input("Set Time")
    formatted_time = med_time.strftime("%I:%M %p")
    
    submit = st.form_submit_button("Add Reminder")

if submit and name:
    new_data = pd.DataFrame([[name, dose, formatted_time, False]], 
                            columns=["Medicine", "Dose", "Time", "Sent"])
    st.session_state.schedule = pd.concat([st.session_state.schedule, new_data], ignore_index=True)
    st.success(f"Reminder set for {name} at {formatted_time}")

st.subheader("Your Schedule")
st.table(st.session_state.schedule)
