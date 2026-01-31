import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- EMAIL FUNCTION ---------------- #
def send_email(to_email, subject, body):
    sender_email = "your_email@gmail.com"      # 🔴 replace
    app_password = "your_app_password"         # 🔴 replace (Gmail App Password)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(e)
        return False


# ---------------- STREAMLIT CONFIG ---------------- #
st.set_page_config("Medicine Reminder", "💊")
st.title("💊 Medicine Reminder (Email Notification)")

# auto refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="refresh")

email = st.text_input("📧 Enter your Email")

# ---------------- SESSION STATE ---------------- #
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# ---------------- ADD MEDICINE ---------------- #
st.subheader("➕ Add Medicine")

medicine_name = st.text_input("Medicine Name")

col1, col2 = st.columns(2)
with col1:
    hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
with col2:
    minute = st.selectbox("Minute", [f"{i:02d}" for i in range(60)])

ampm = st.selectbox("AM / PM", ["AM", "PM"])

medicine_time = f"{hour}:{minute} {ampm}"

if st.button("Add Medicine"):
    if medicine




