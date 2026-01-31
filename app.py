pip install streamlit schedule
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import threading
from datetime import datetime

# --- Configuration ---
# REPLACE WITH YOUR EMAIL/APP PASSWORD
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # 16-char app password
RECEIVER_EMAIL = "recipient_email@gmail.com"

# --- Functions ---
def send_email(med_name, med_time):
    """Sends an email notification."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"💊 Medicine Reminder: {med_name}"
    body = f"It's time to take your medicine: {med_name} at {med_time}. Please do not forget!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)

def scheduler_thread():
    """Runs the scheduler in a separate thread."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- Streamlit UI ---
st.set_page_config(page_title="Medicine Reminder", page_icon="💊")
st.title("💊 Automated Medicine Reminder")

# Initialize session state for storing multiple medicines
if 'medicines' not in st.session_state:
    st.session_state['medicines'] = []

# Input Form
with st.form("add_medicine_form"):
    st.subheader("Add New Medicine")
    med_name = st.text_input("Medicine Name", placeholder="e.g., Paracetamol")
    col1, col2 = st.columns(2)
    with col1:
        med_time = st.time_input("Reminder Time")
    with col2:
        # Format time to AM/PM for display
        formatted_time = med_time.strftime("%I:%M %p")
        st.write(f"Scheduled for: **{formatted_time}**")
    
    submit = st.form_submit_button("Add to Schedule")

if submit and med_name:
    st.session_state['medicines'].append({
        "name": med_name,
        "time": formatted_time
    })
    
    # Schedule the job
    schedule.every().day.at(med_time.strftime("%H:%M")).do(
        send_email, med_name=med_name, med_time=formatted_time
    )
    st.success(f"Reminder set for {med_name} at {formatted_time}")

# Display Scheduled Medicines
st.divider()
st.subheader("Current Schedule")
if st.session_state['medicines']:
    for med in st.session_state['medicines']:
        st.info(f"💊 **{med['name']}** - {med['time']}")
else:
    st.warning("No medicines added yet.")

# Start scheduler in background if not already running
if 'scheduler_started' not in st.session_state:
    threading.Thread(target=scheduler_thread, daemon=True).start()
    st.session_state['scheduler_started'] = True

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Enter the medicine name.
2. Select the time (AM/PM).
3. Click 'Add to Schedule'.
4. Keep this app running to receive email alerts.
""")





























