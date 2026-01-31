import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import threading

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email
SENDER_PASSWORD = "your_app_password"  # Replace with your 16-char App Password
RECEIVER_EMAIL = "recipient_email@gmail.com" # Replace with receiver's email

def send_email(med_name, med_time):
    """Sends an email notification."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"💊 Medicine Reminder: {med_name}"
    body = f"Hello,\n\nThis is a reminder to take your medicine: {med_name} at {med_time}.\n\nStay healthy!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent for {med_name}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- STREAMLIT UI ---
st.set_page_config(page_title="💊 Medicine Reminder", page_icon="💊")
st.title("💊 Automated Medicine Reminder")

# Session state to store multiple medicines
if 'medicines' not in st.session_state:
    st.session_state['medicines'] = []

with st.form("medicine_form"):
    st.subheader("Add New Medicine")
    med_name = st.text_input("Medicine Name")
    col1, col2, col3 = st.columns(3)
    with col1:
        hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    with col2:
        minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60, 5)])
    with col3:
        ampm = st.selectbox("AM/PM", ["AM", "PM"])
    
    time_str = f"{hour}:{minute} {ampm}"
    submit = st.form_submit_button("Add Reminder")

    if submit and med_name:
        st.session_state['medicines'].append({"name": med_name, "time": time_str})
        st.success(f"Added {med_name} at {time_str}")

# Display Scheduled Medicines
st.subheader("Scheduled Medicines")
if st.session_state['medicines']:
    for i, med in enumerate(st.session_state['medicines']):
        st.write(f"{i+1}. **{med['name']}** - {med['time']}")
else:
    st.info("No medicines added yet.")

# --- BACKGROUND SCHEDULER ---
def run_scheduler():
    while True:
        now = datetime.datetime.now().strftime("%I:%M %p")
        for med in st.session_state['medicines']:
            if now == med['time']:
                send_email(med['name'], med['time'])
                time.sleep(60) # Prevent multiple emails in the same minute
        time.sleep(10) # Check every 10 seconds

# Run scheduler in a separate thread
if 'thread_started' not in st.session_state:
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    st.session_state['thread_started'] = True


