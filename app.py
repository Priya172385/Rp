import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

# --- CONFIGURATION (Use App Password for Gmail) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # Use app password
RECEIVER_EMAIL = "receiver_email@gmail.com"

# --- EMAIL SENDING FUNCTION ---
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
        st.error(f"Error: {e}")
        return False

# --- STREAMLIT UI ---
st.title("💊 Automated Medicine Reminder")

st.sidebar.header("Add New Medicine")
med_name = st.sidebar.text_input("Medicine Name")
dosage = st.sidebar.text_input("Dosage (e.g., 1 tablet)")
time_input = st.sidebar.time_input("Set Time (AM/PM)", value=None)

if st.sidebar.button("Add Reminder"):
    if med_name and time_input:
        # Store in session state for persistence
        if 'reminders' not in st.session_state:
            st.session_state['reminders'] = []
        
        # Format time to AM/PM
        formatted_time = time_input.strftime("%I:%M %p")
        st.session_state['reminders'].append({
            "name": med_name,
            "dosage": dosage,
            "time": formatted_time
        })
        st.sidebar.success(f"Reminder set for {med_name} at {formatted_time}")
    else:
        st.sidebar.error("Please fill in Medicine Name and Time")

# --- DISPLAY REMINDERS ---
st.subheader("Current Reminders")
if 'reminders' in st.session_state and st.session_state['reminders']:
    for i, rem in enumerate(st.session_state['reminders']):
        st.write(f"{i+1}. **{rem['name']}** ({rem['dosage']}) - {rem['time']}")
    
    # --- AUTOMATION LOGIC ---
    if st.button("Start Reminder System"):
        st.info("System Running... Checking times every minute.")
        while True:
            now = datetime.now().strftime("%I:%M %p")
            for rem in st.session_state['reminders']:
                if now == rem['time']:
                    subject = f"🔔 MEDICATION REMINDER: {rem['name']}"
                    body = f"Time to take your medicine!\n\nMedicine: {rem['name']}\nDosage: {rem['dosage']}\nTime: {rem['time']}"
                    if send_email(subject, body):
                        st.success(f"Email sent for {rem['name']} at {now}")
                    time.sleep(60) # Prevent multiple emails in one minute
            time.sleep(10) # Check every 10 seconds
else:
    st.write("No reminders set yet.")

























