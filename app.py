import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- CONFIGURATION ---------------- #
# USE YOUR 16-DIGIT APP PASSWORD HERE (NO SPACES)
SENDER_EMAIL = "your_email@gmail.com"  
APP_PASSWORD = "swwq etft wbah jddd" 

# Global variables to ensure the background thread can see them
if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []

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
        print(f"SMTP Error: {e}") # This will show in your terminal
        return False

# ---------------- BACKGROUND CHECKER ---------------- #
def reminder_loop(user_email):
    """Checks for reminders every 30 seconds"""
    while True:
        current_time = datetime.now().strftime("%I:%M %p")
        
        # We loop through the list in session state
        for med in st.session_state.medicine_list:
            if med["time"] == current_time and not med["sent"]:
                body = f"💊 Reminder: Time to take {med['name']}!"
                if send_email(user_email, "Medicine Alert", body):
                    med["sent"] = True
                    print(f"Email sent successfully to {user_email}")
        
        time.sleep(30)

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Meds Notify", page_icon="💊")
st.title("💊 Medicine Email Reminder")

email_target = st.text_input("📧 Receiver Email", placeholder="Where should we send the alerts?")

with st.form("med_add"):
    name = st.text_input("Medicine Name")
    c1, c2, c3 = st.columns(3)
    hr = c1.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    mn = c2.selectbox("Min", [f"{i:02d}" for i in range(0, 60)])
    ap = c3.selectbox("AM/PM", ["AM", "PM"])
    
    if st.form_submit_button("Add Medicine"):
        if name:
            st.session_state.medicine_list.append({
                "name": name, 
                "time": f"{hr}:{mn} {ap}", 
                "sent": False
            })
            st.success(f"Added {name}")

# Show Schedule
for m in st.session_state.medicine_list:
    st.write(f"⏰ {m['time']} - {m['name']} ({'✅ Sent' if m['sent'] else '⏳ Pending'})")

# Start Threading
if st.button("🚀 Start Reminder Service"):
    if email_target and not st.session_state.get("running"):
        thread = threading.Thread(target=reminder_loop, args=(email_target,), daemon=True)
        thread.start()
        st.session_state["running"] = True
        st.success("Service Started! Keep this tab open.")
    elif not email_target:
        st.error("Please enter a receiver email.")




