import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- CONFIGURATION ---------------- #
SENDER_EMAIL = "your_email@gmail.com"  # <--- Change this
APP_PASSWORD = "xxxx xxxx xxxx xxxx"    # <--- Use the 16-digit App Password

# ---------------- EMAIL FUNCTION ---------------- #
def send_email(receiver_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        # Using Port 465 for SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# ---------------- BACKGROUND CHECKER ---------------- #
def reminder_loop():
    """Checks for reminders every 30 seconds without blocking the UI"""
    while True:
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Check the global list stored in session state
        if "medicine_list" in st.session_state:
            for med in st.session_state.medicine_list:
                if med["time"] == current_time and not med["sent"]:
                    success = send_email(
                        st.session_state.user_email, 
                        "💊 Medicine Reminder", 
                        f"Time to take: {med['name']}\nScheduled for: {med['time']}"
                    )
                    if success:
                        med["sent"] = True
        
        time.sleep(30) # Wait 30 seconds before checking again

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="MedsRemind", page_icon="💊")
st.title("💊 Medicine Email Reminder")

# Initialize Session States so data isn't lost on refresh
if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []
if "thread_started" not in st.session_state:
    st.session_state.thread_started = False

st.session_state.user_email = st.text_input("📧 Your Receiving Email Address", placeholder="where to send alerts?")

with st.expander("➕ Add New Medicine"):
    m_name = st.text_input("Medicine Name")
    c1, c2, c3 = st.columns(3)
    hr = c1.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    mn = c2.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])
    ap = c3.selectbox("AM/PM", ["AM", "PM"])
    
    if st.button("Add to Schedule"):
        if m_name and st.session_state.user_email:
            new_med = {"name": m_name, "time": f"{hr}:{mn} {ap}", "sent": False}
            st.session_state.medicine_list.append(new_med)
            st.success(f"Added {m_name} at {hr}:{mn} {ap}")
        else:
            st.error("Please provide a name and email.")

# Display Current Schedule
st.subheader("📋 Your Schedule")
if not st.session_state.medicine_list:
    st.info("No medicines added.")
else:
    for med in st.session_state.medicine_list:
        status = "✅ Sent" if med['sent'] else "⏳ Waiting"
        st.write(f"**{med['time']}** — {med['name']} ({status})")

# ---------------- START BUTTON ---------------- #
if not st.session_state.thread_started:
    if st.button("🚀 Start Reminder System"):
        if st.session_state.user_email:
            # Create and start the background thread
            bg_thread = threading.Thread(target=reminder_loop, daemon=True)
            bg_thread.start()
            st.session_state.thread_started = True
            st.success("System is now running in the background!")
        else:
            st.warning("Enter an email first.")




