import streamlit as st
import smtplib
import schedule
import time
import threading
from email.mime.text import MIMEText
from datetime import datetime

# --- Configuration ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com" # Update this
SENDER_PASSWORD = "your_app_password"   # Update this (App Password)
RECEIVER_EMAIL = "receiver_email@gmail.com" # Update this

# --- Functions ---
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def schedule_reminders():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- Initialize session state ---
if 'meds' not in st.session_state:
    st.session_state['meds'] = []

# --- UI Setup ---
st.title("💊 Automated Medicine Reminder")

with st.sidebar:
    st.header("Add New Medicine")
    med_name = st.text_input("Medicine Name")
    time_input = st.time_input("Time", value=None)
    am_pm = st.selectbox("AM/PM", ["AM", "PM"])
    
    if st.button("Add Reminder"):
        if med_name and time_input:
            formatted_time = time_input.strftime("%I:%M %p")
            st.session_state['meds'].append({
                "name": med_name,
                "time": formatted_time
            })
            st.success(f"Added: {med_name} at {formatted_time}")
            
            # Schedule the task
            schedule.every().day.at(time_input.strftime("%H:%M")).do(
                send_email,
                subject=f"Medicine Reminder: {med_name}",
                body=f"Time to take your {med_name} at {formatted_time}!"
            )
        else:
            st.error("Please fill in all fields.")

# --- Display Meds ---
st.subheader("Your Schedule")
if st.session_state['meds']:
    for med in st.session_state['meds']:
        st.write(f"- **{med['name']}** at **{med['time']}**")
else:
    st.info("No medicines added yet.")

# --- Start Scheduler ---
if 'thread_started' not in st.session_state:
    t = threading.Thread(target=schedule_reminders, daemon=True)
    t.start()
    st.session_state['thread_started'] = True
    st.sidebar.success("Scheduler Active")
























