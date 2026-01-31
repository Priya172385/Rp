import streamlit as st
import schedule
import time
import threading
from twilio.rest import Client

# --- Streamlit UI Setup ---
st.set_page_config(page_title="MedRemind SMS", page_icon="💊")
st.title("💊 Medicine SMS Reminder")

# --- Twilio Configuration (Securely entered via Sidebar) ---
with st.sidebar:
    st.header("Setup Credentials")
    sid = st.text_input("Twilio SID", type="password")
    token = st.text_input("Twilio Auth Token", type="password")
    t_num = st.text_input("Twilio Phone Number")
    u_num = st.text_input("Your Phone Number (with +country code)")

# --- Backend Reminder Logic ---
def send_sms(med_name, dosage):
    try:
        client = Client(sid, token)
        client.messages.create(
            body=f"REMINDER: Take {dosage} of {med_name} now!",
            from_=t_num,
            to=u_num
        )
        print(f"Success: Sent {med_name} reminder.")
    except Exception as e:
        print(f"Error: {e}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(10)

# Start background thread for the scheduler once
if 'scheduler_started' not in st.session_state:
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    st.session_state['scheduler_started'] = True
    st.session_state['meds'] = []

# --- User Interface ---
with st.form("med_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        med_name = st.text_input("Medicine Name")
    with col2:
        dosage = st.text_input("Dosage (e.g. 1 pill)")
    with col3:
        rem_time = st.time_input("Reminder Time")
    
    submit = st.form_submit_button("Add Reminder")

if submit and med_name and sid:
    formatted_time = rem_time.strftime("%H:%M")
    # Schedule the task
    schedule.every().day.at(formatted_time).do(send_sms, med_name=med_name, dosage=dosage)
    # Save to local session state for display
    st.session_state['meds'].append({"name": med_name, "time": formatted_time, "dose": dosage})
    st.success(f"Reminder set for {med_name} at {formatted_time}")

# --- Display Active Reminders ---
st.subheader("Your Active Schedule")
if st.session_state['meds']:
    for m in st.session_state['meds']:
        st.write(f"⏰ **{m['time']}** - {m['name']} ({m['dose']})")
else:
    st.info("No reminders set yet.")

















