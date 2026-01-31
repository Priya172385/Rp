pip install streamlit streamlit-autorefresh
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- EMAIL FUNCTION ---------------- #
def send_email(receiver_email, subject, message):
    sender_email = "your_email@gmail.com"      # 🔴 change
    app_password = "your_app_password"         # 🔴 change (Gmail App Password)

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
        st.error(f"Email error: {e}")
        return False


# ---------------- STREAMLIT CONFIG ---------------- #
st.set_page_config(page_title="Medicine Reminder", layout="centered")
st.title("💊 Medicine Reminder App (Email Notification)")

# refresh app every 60 seconds
st_autorefresh(interval=60 * 1000, key="auto_refresh")

email = st.text_input("📧 Enter your Email")

# ---------------- ADD MEDICINE ---------------- #
st.subheader("Add Medicine")

medicine_name = st.text_input("Medicine Name")

col1, col2 = st.columns(2)
with col1:
    hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
with col2:
    minute = st.selectbox("Minute", [f"{i:02d}" for i in range(60)])

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
        st.success("Medicine added successfully!")
    else:
        st.error("Please enter medicine name")

# ---------------- SHOW MEDICINES ---------------- #
st.subheader("📋 Medicine Schedule")
if st.session_state.medicine_list:
    for med in st.session_state.medicine_list:
        st.write(f"• {med['name']} at {med['time']}")
else:
    st.info("No medicines added yet")

# ---------------- REMINDER CHECK ---------------- #
current_time = datetime.now().strftime("%I:%M %p")

for med in st.session_state.medicine_list:
    if med["time"] == current_time and not med["sent"] and email:
        message = (
            f"💊 Medicine Reminder\n\n"
            f"Medicine: {med['name']}\n"
            f"Time: {med['time']}\n\n"
            "Please take your medicine on time."
        )

        if send_email(email, "💊 Medicine Reminder", message):
            med["sent"] = True
            st.success(f"Reminder email sent for {med['name']}")



