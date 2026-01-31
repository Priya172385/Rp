import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

# ---------------- EMAIL FUNCTION ---------------- #
def send_email(receiver_email, subject, message):
    sender_email = "your_email@gmail.com"        # CHANGE THIS
    app_password = "your_app_password"           # CHANGE THIS

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(e)
        return False

# ---------------- REMINDER CHECKER ---------------- #
def reminder_checker(medicine_list, email):
    while True:
        current_time = datetime.now().strftime("%I:%M %p")
        for med in medicine_list:
            if med["time"] == current_time and not med["sent"]:
                message = f"💊 Medicine Reminder\n\nMedicine: {med['name']}\nTime: {med['time']}"
                if send_email(email, "Medicine Reminder", message):
                    med["sent"] = True
        time.sleep(60)

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Medicine Reminder", layout="centered")
st.title("💊 Medicine Reminder App (Email Notification)")

email = st.text_input("📧 Enter your Email")

st.subheader("Add Medicine")

medicine_name = st.text_input("Medicine Name")

col1, col2 = st.columns(2)
with col1:
    hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
with col2:
    minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])

ampm = st.selectbox("AM / PM", ["AM", "PM"])

medicine_time = f"{hour}:{minute} {ampm}"

if "medicine_list" not in st.session_state:
    st.session_state.medicine_list = []

if st.button("➕ Add Medicine"):
    if medicine_name:
        st.session_state.medicine_list.append({
            "name": medicine_name,
            "time": medicine_time,
            "sent": False
        })
        st.success("Medicine Added!")
    else:
        st.error("Please enter medicine name")

# ---------------- DISPLAY MEDICINES ---------------- #
st.subheader("📋 Medicine Schedule")
for med in st.session_state.medicine_list:
    st.write(f"• {med['name']} at {med['time']}")

# ---------------- START REMINDER ---------------- #
if st.button("🚀 Start Reminder"):
    if email and st.session_state.medicine_list:
        thread = threading.Thread(
            target=reminder_checker,
            args=(st.session_state.medicine_list, email),
            daemon=True
        )
        thread.start()
        st.success("Reminder Started! You will receive emails on time.")
    else:
        st.error("Please enter email and add medicines")

