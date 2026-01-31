import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- CONFIGURATION ---------------- #
# 1. Go to Google Account -> Security
# 2. Enable 2-Step Verification
# 3. Search for "App Passwords" and create one for "Mail"
SENDER_EMAIL = "your_email@gmail.com" 
APP_PASSWORD = "your_app_password" 

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
        print(f"Error sending email: {e}")
        return False

# ---------------- BACKGROUND CHECKER ---------------- #
def reminder_loop():
    """Background task that checks for reminders every 30 seconds"""
    while True:
        # Use st.session_state carefully or a global list
        # For simplicity in background threads, we check the global state
        current_time = datetime.now().strftime("%I:%M %p")
        
        if "medicine_list" in st.session_state:
            for med in st.session_state.medicine_list:
                if med["time"] == current_time and not med["sent"]:
                    success = send_email(st.session_state.user_email, "💊 Medicine Reminder", 
                                        f"Time to take your medicine: {med['name']}")
                    if success:
                        med["sent"] = True
                        print(f"Reminder sent for {med['name']} at {current_time}")
        
        time.sleep(30) # Check twice a minute to avoid missing the window

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="MedsRemind", page_icon="💊")
st.title("💊 Medicine Email Reminder")

# Initialize Session States
if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []
if "thread_started" not in st.session_state:
    st.session_state.thread_started = False

st.session_state.user_email = st.text_input("📧 Your Email Address", placeholder="example@mail.com")

with st.expander("➕ Add New Medicine"):
    m_name = st.text_input("Medicine Name")
    c1, c2, c3 = st.columns(3)
    hr = c1.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    mn = c2.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])
    ap = c3.selectbox("AM/PM", ["AM", "PM"])
    
    if st.button("Save Medicine"):
        if m_name and st.session_state.user_email:
            new_med = {"name": m_name, "time": f"{hr}:{mn} {ap}", "sent": False}
            st.session_state.medicine_list.append(new_med)
            st.success(f"Added {m_name}!")
        else:
            st.error("Please fill in all fields.")

# Display Schedule
st.subheader("📋 Your Schedule")
if not st.session_state.medicine_list:
    st.info("No medicines added yet.")
else:
    for med in st.session_state.medicine_list:
        status = "✅ Sent" if med['sent'] else "⏳ Pending"
        st.write(f"**{med['time']}** - {med['name']} ({status})")

# ---------------- START THREAD ---------------- #
if not st.session_state.thread_started:
    if st.button("🚀 Activate Reminder System"):
        daemon_thread = threading.Thread(target=reminder_loop, daemon=True)
        daemon_thread.start()
        st.session_state.thread_started = True
        st.success("System is now live in the background!")




