import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- CONFIGURATION ---------------- #
# IMPORTANT: Put your 16-character App Password here (no spaces)
SENDER_EMAIL = "your_email@gmail.com"  
APP_PASSWORD = "your_app_password_here" 

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
        st.error(f"Email Error: {e}")
        return False

# ---------------- BACKGROUND CHECKER ---------------- #
def reminder_loop(user_email):
    while True:
        now = datetime.now().strftime("%I:%M %p")
        # Accessing session_state inside a thread can be unstable in Streamlit
        # but for local use, it works if the session is active.
        if "medicine_list" in st.session_state:
            for med in st.session_state.medicine_list:
                if med["time"] == now and not med["sent"]:
                    body = f"💊 Medicine Reminder!\n\nIt is {now}. Time to take: {med['name']}"
                    if send_email(user_email, "Medicine Alert", body):
                        med["sent"] = True
        time.sleep(30)

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Medicine Notify", page_icon="💊")
st.title("💊 Medicine Email Reminder")

# Setup state
if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []
if "running" not in st.session_state:
    st.session_state.running = False

email_target = st.text_input("📧 Receiver Email Address")

# TEST BUTTON: Check connection immediately
if st.button("🧪 Send Test Email"):
    if email_target:
        if send_email(email_target, "Test Email", "If you see this, your settings are CORRECT!"):
            st.success("Test email sent! Check your inbox (and Spam).")
    else:
        st.warning("Enter an email first.")

with st.expander("➕ Add Medicine"):
    name = st.text_input("Medicine Name")
    c1, c2, c3 = st.columns(3)
    hr = c1.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    mn = c2.selectbox("Min", [f"{i:02d}" for i in range(0, 60)])
    ap = c3.selectbox("AM/PM", ["AM", "PM"])
    
    if st.button("Save"):
        st.session_state.medicine_list.append({"name": name, "time": f"{hr}:{mn} {ap}", "sent": False})
        st.success("Added!")

# Display List
for m in st.session_state.medicine_list:
    st.write(f"⏰ {m['time']} - {m['name']} {'✅' if m['sent'] else '⏳'}")

# Start the Service
if not st.session_state.running:
    if st.button("🚀 Start Reminder Service"):
        if email_target:
            t = threading.Thread(target=reminder_loop, args=(email_target,), daemon=True)
            t.start()
            st.session_state.running = True
            st.success("System Live! Don't close this browser tab.")
