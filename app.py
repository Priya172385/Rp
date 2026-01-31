import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- CONFIGURATION ---------------- #
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your Gmail
APP_PASSWORD = "xxxx xxxx xxxx xxxx"    # Replace with your 16-digit App Password

# Global list to share data between Streamlit and the background thread
# This is necessary because threads can't see st.session_state reliably
PENDING_MEDS = []
USER_EMAIL_TARGET = ""

# ---------------- EMAIL FUNCTION ---------------- #
def send_email(receiver_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# ---------------- BACKGROUND CHECKER ---------------- #
def reminder_loop():
    """Checks for reminders every 30 seconds"""
    global PENDING_MEDS, USER_EMAIL_TARGET
    while True:
        now = datetime.now().strftime("%I:%M %p")
        
        for med in PENDING_MEDS:
            if med["time"] == now and not med["sent"]:
                # Attempt to send email
                if USER_EMAIL_TARGET:
                    body = f"Hello! This is your reminder to take: {med['name']} at {med['time']}."
                    success = send_email(USER_EMAIL_TARGET, "💊 Medicine Reminder", body)
                    if success:
                        med["sent"] = True
                        print(f"SENT: {med['name']}")
        
        time.sleep(30) # Check twice a minute

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="MedsRemind", layout="centered")
st.title("💊 Medicine Email Reminder")

# Setup Global State
if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []
if "running" not in st.session_state:
    st.session_state.running = False

# Input Email
email_input = st.text_input("📧 Enter Your Email Address (Receiver)")

# Add Medicine Form
with st.form("med_form", clear_on_submit=True):
    name = st.text_input("Medicine Name")
    col1, col2, col3 = st.columns(3)
    hr = col1.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    mn = col2.selectbox("Min", [f"{i:02d}" for i in range(0, 60)])
    ap = col3.selectbox("AM/PM", ["AM", "PM"])
    
    submitted = st.form_submit_button("Add Medicine")
    if submitted and name:
        new_med = {"name": name, "time": f"{hr}:{mn} {ap}", "sent": False}
        st.session_state.medicine_list.append(new_med)
        PENDING_MEDS.append(new_med) # Update the global thread list
        st.success(f"Added {name}!")

# Display Schedule
st.subheader("📋 Scheduled Medicines")
for m in st.session_state.medicine_list:
    status = "✅ Sent" if m['sent'] else "⏳ Waiting"
    st.write(f"{m['time']} - **{m['name']}** [{status}]")

# Start Thread
if not st.session_state.running:
    if st.button("🚀 Start Reminder Service"):
        if email_input:
            USER_EMAIL_TARGET = email_input # Set the target for the thread
            # Start the background daemon
            thread = threading.Thread(target=reminder_loop, daemon=True)
            thread.start()
            st.session_state.running = True




