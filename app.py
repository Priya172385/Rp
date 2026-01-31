import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

# --- Email Configuration ---
# Use an App Password for Gmail, not your regular password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # Generated from Google Account

def send_email(receiver_email, medicine_name, dosage):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = f"💊 Medicine Reminder: {medicine_name}"
    
    body = f"Hello,\n\nIt's time to take your medicine:\n\nMedicine: {medicine_name}\nDosage: {dosage}\n\nStay healthy!"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# --- Streamlit UI ---
st.title("💊 Automated Medicine Reminder")

with st.form("reminder_form"):
    patient_email = st.text_input("Patient Email")
    medicine_name = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage (e.g., 1 pill, 5ml)")
    reminder_time = st.time_input("Set Reminder Time")
    submitted = st.form_submit_button("Schedule Reminder")

if submitted:
    st.write(f"Waiting to send reminder at {reminder_time}...")
    
    # Simple scheduler loop (for demonstration, better to use background task scheduler)
    while True:
        now = datetime.now().time()
        if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
            success = send_email(patient_email, medicine_name, dosage)
            if success:
                st.success("✅ Reminder email sent successfully!")
            break
        time.sleep(30) # Check every 30 seconds






















