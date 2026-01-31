import streamlit as st
import schedule
import time
import threading
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Email Med-Reminder", page_icon="📧")
st.title("📧 Medicine Email Reminder")

# --- Initialize States ---
if 'reminders' not in st.session_state:
    st.session_state['reminders'] = []
if 'scheduler_running' not in st.session_state:
    st.session_state['scheduler_running'] = False

# --- Email Logic ---
def send_email(med_name, dosage, sender_email, app_password, receiver_email):
    msg = EmailMessage()
    msg.set_content(f"Hello!\n\nThis is your reminder to take {dosage} of {med_name}.\n\nStay healthy!")
    msg['Subject'] = f"💊 Medicine Reminder: {med_name}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print(f"Email sent for {med_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

# --- Background Scheduler ---
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(5)

if not st.session_state['scheduler_running']:
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    st.session_state['scheduler_running'] = True

# --- UI Sidebar ---
with st.sidebar:
    st.header("⚙️ Email Configuration")
    s_email = st.text_input("Your Gmail Address")
    a_pass = st.text_input("App Password", type="password", help="The 16-character code from Google")
    r_email = st.text_input("Receiver Email (can be same as your gmail)")

# --- Main Interface ---
with st.form("med_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    name = col1.text_input("Medicine Name")
    dose = col2.text_input("Dosage")
    rem_time = st.time_input("Time for Reminder")
    
    if st.form_submit_button("Add Reminder"):
        if s_email and a_pass:
            t_str = rem_time.strftime("%H:%M")
            schedule.every().day.at(t_str).do(
                send_email, 
                med_name=name, 
                dosage=dose, 
                sender_email=s_email, 
                app_password=a_pass, 
                receiver_email=r_email
            )
            st.session_state['reminders'].append({"name": name, "dose": dose, "time": t_str})
            st.success(f"Reminder set for {name} at {t_str}")
        else:
            st.error("Please provide email credentials in the sidebar.")

# --- Display List ---
st.subheader("📋 Active Reminders")
for r in st.session_state['reminders']:
    st.write(f"⏰ **{r['time']}** — {r['name']} ({r['dose']})")



















