import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Functions ---
def send_email(subject, body, to_email):
    # Configure your SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "YOUR_EMAIL@gmail.com" # Replace with your email
    sender_password = "YOUR_APP_PASSWORD"   # Replace with your app password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# --- UI Setup ---
st.title("💊 Automated Medicine Reminder")

with st.form("reminder_form"):
    med_name = st.text_input("Medicine Name")
    user_email = st.text_input("Recipient Email Address")
    remind_time = st.time_input("Reminder Time")
    submit = st.form_submit_button("Set Reminder")

    if submit:
        if med_name and user_email:
            subject = f"🔔 Reminder: Take {med_name}"
            body = f"Hello, it's time to take your medicine: {med_name} at {remind_time}."
            
            with st.spinner('Sending email...'):
                success = send_email(subject, body, user_email)
                if success:
                    st.success(f"Reminder set for {med_name} at {remind_time}! Email will be sent.")
        else:
            st.warning("Please fill in all fields.")

# --- How to Run ---
# Save as app.py
# Run: streamlit run app.py





















