import streamlit as st
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configuration (Error-free Email Setup) ---
# Use App Passwords for Gmail if 2FA is enabled
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # Use App Password, not main password

# --- Email Function ---
def send_email_reminder(recipient, medicine_name, dosage):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = f"🚨 Medicine Reminder: {medicine_name}"
    
    body = f"Hello,\n\nIt is time to take your medicine:\n{medicine_name} - {dosage}\n\nStay healthy!"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# --- Streamlit UI ---
st.title("💊 Automated Medicine Reminder")

with st.form("reminder_form"):
    med_name = st.text_input("Medicine Name", placeholder="E.g., Paracetamol")
    dosage = st.text_input("Dosage", placeholder="E.g., 500mg, 1 tablet")
    recipient_email = st.text_input("Recipient Email")
    time_input = st.time_input("Reminder Time (AM/PM)")
    submit = st.form_submit_button("Set Reminder")

if submit:
    if med_name and recipient_email:
        st.success(f"Reminder set for {med_name} at {time_input.strftime('%I:%M %p')}")
        # Store reminder logic (simplified for example)
        # In production, use a database or scheduler (e.g., APScheduler)
    else:
        st.error("Please fill in all fields.")

# --- Background Task Simulation ---
if st.button("Simulate Immediate Email"):
    with st.spinner("Sending email..."):
        success = send_email_reminder(recipient_email, med_name, dosage)
        if success:
            st.success("Email sent successfully!")

# To run: streamlit run app.py
