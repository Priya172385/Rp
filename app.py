import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

# --- CONFIGURATION (Change this) ---
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # 16-character app password
RECEIVER_EMAIL = "recipient_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# ----------------------------------

st.set_page_config(page_title="Medicine Reminder", page_icon="💊")

# Initialize session state for storing medicines
if 'medicines' not in st.session_state:
    st.session_state['medicines'] = []

def send_email_notification(med_name, med_time):
    """Sends an email notification."""
    msg = MIMEText(f"Reminder: It's time to take your medication: {med_name} at {med_time}.")
    msg['Subject'] = f"💊 Medicine Reminder: {med_name}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# --- App UI ---
st.title("💊 Medicine Reminder System")

with st.sidebar:
    st.header("Add New Medicine")
    med_name = st.text_input("Medicine Name", placeholder="e.g., Paracetamol")
    
    # Time picker (AM/PM)
    col1, col2 = st.columns(2)
    with col1:
        hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
        minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60, 5)])
    with col2:
        am_pm = st.selectbox("AM/PM", ["AM", "PM"])
    
    med_time = f"{hour}:{minute} {am_pm}"
    
    if st.button("Add Reminder"):
        if med_name:
            st.session_state['medicines'].append({"name": med_name, "time": med_time})
            st.success(f"Added {med_name} at {med_time}")
        else:
            st.warning("Please enter a medicine name")

# --- Display Schedule ---
st.header("Current Schedule")
if not st.session_state['medicines']:
    st.info("No medicines added yet.")
else:
    for i, med in enumerate(st.session_state['medicines']):
        st.write(f"**{i+1}. {med['name']}** - {med['time']}")

# --- Simulation/Notification Logic ---
st.header("Active Reminders")
if st.button("Check/Send Now (Simulation)"):
    for med in st.session_state['medicines']:
        with st.spinner(f"Sending reminder for {med['name']}..."):
            if send_email_notification(med['name'], med['time']):
                st.success(f"Sent: {med['name']} at {med['time']}")
    st.info("In a real scenario, this would run in the background based on system time.")

st.markdown("---")
st.write("💡 *Note: To make this fully automatic, this script should run on a server with a task scheduler like `cron` or Celery.*")




























