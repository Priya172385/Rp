import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import threading

# -------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = ""

if "password" not in st.session_state:
    st.session_state.password = ""

if "medicines" not in st.session_state:
    st.session_state.medicines = []

if "thread_started" not in st.session_state:
    st.session_state.thread_started = False


# -------------------------------------------------
# EMAIL FUNCTION
# -------------------------------------------------
def send_email(sender_email, sender_password, receiver_email, med_name, med_time):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"💊 Medicine Reminder: {med_name}"

    body = f"""
Hello,

This is your medicine reminder.

Medicine Name : {med_name}
Time          : {med_time}

Please take your medicine on time.
Stay healthy 💙
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Email sent for {med_name}")
    except Exception as e:
        print("Email error:", e)


# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
st.set_page_config(page_title="💊 Medicine Reminder", page_icon="💊")

if not st.session_state.logged_in:
    st.title("🔐 Login")
    st.write("Enter your **Gmail** and **App Password**")

    email = st.text_input("📧 Gmail Address")
    password = st.text_input("🔑 Gmail App Password", type="password")

    login_btn = st.button("Login")

    if login_btn:
        if email and password:
            st.session_state.email = email
            st.session_state.password = password
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Please enter both email and app password")

    st.info(
        "⚠️ Use **Gmail App Password**, not your normal Gmail password.\n\n"
        "Google Account → Security → App Passwords"
    )

    st.stop()


# -------------------------------------------------
# MAIN APP (AFTER LOGIN)
# -------------------------------------------------
st.title("💊 Automated Medicine Reminder")
st.write(f"Logged in as **{st.session_state.email}**")

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.medicines = []
    st.session_state.thread_started = False
    st.rerun()

# -------------------------------------------------
# ADD MEDICINE FORM
# -------------------------------------------------
with st.form("medicine_form"):
    st.subheader("Add New Medicine")

    med_name = st.text_input("Medicine Name")

    col1, col2, col3 = st.columns(3)
    with col1:
        hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    with col2:
        minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60, 5)])
    with col3:
        ampm = st.selectbox("AM / PM", ["AM", "PM"])

    time_str = f"{hour}:{minute} {ampm}"
    submit = st.form_submit_button("➕ Add Reminder")

    if submit and med_name:
        st.session_state.medicines.append(
            {"name": med_name, "time": time_str}
        )
        st.success(f"Added **{med_name}** at **{time_str}**")


# -------------------------------------------------
# DISPLAY MEDICINES
# -------------------------------------------------
st.subheader("📋 Scheduled Medicines")

if st.session_state.medicines:
    for i, med in enumerate(st.session_state.medicines):
        st.write(f"{i+1}. **{med['name']}** — ⏰ {med['time']}")
else:
    st.info("No medicines added yet.")


# -------------------------------------------------
# BACKGROUND SCHEDULER
# -------------------------------------------------
def run_scheduler():
    while True:
        now = datetime.datetime.now().strftime("%I:%M %p")

        for med in st.session_state.medicines:
            if now == med["time"]:
                send_email(
                    st.session_state.email,
                    st.session_state.password,
                    st.session_state.email,
                    med["name"],
                    med["time"]
                )
                time.sleep(60)  # avoid duplicate emails

        time.sleep(10)


if not st.session_state.thread_started:
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    st.session_state.thread_started = True
