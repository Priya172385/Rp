pip install twilio streamlit
import streamlit as st
from twilio.rest import Client
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="💊 Medicine Reminder", page_icon="💊")
st.title("💊 Medicine Reminder with Phone SMS Notifications")

# -------------------
# Twilio Configuration
# -------------------
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number

try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    st.error(f"Error connecting to Twilio: {e}")

# -------------------
# User Phone Input
# -------------------
user_phone = st.text_input(
    "Enter your phone number (with country code, e.g., +911234567890)"
)

# -------------------
# Initialize Medicine List
# -------------------
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# -------------------
# Add Medicine Form
# -------------------
st.subheader("Add a Medicine")
with st.form("medicine_form"):
    med_name = st.text_input("Medicine Name")
    med_hour = st.number_input("Hour (0-23)", 0, 23)
    med_minute = st.number_input("Minute (0-59)", 0, 59)
    submitted = st.form_submit_button("Add Medicine")

    if submitted:
        if med_name.strip() == "" or not user_phone:
            st.error("Please enter a medicine name and your phone number!")
        else:
            st.session_state.medicines.append({
                "Medicine": med_name,
                "Hour": med_hour,
                "Minute": med_minute
            })
            st.success(f"Medicine '{med_name}' added at {med_hour:02d}:{med_minute:02d}!")

# -------------------
# Show Medicine Schedule
# -------------------
if st.session_state.medicines:
    st.subheader("🗓️ Medicine Schedule")
    df = pd.DataFrame(st.session_state.medicines)
    st.dataframe(df)

# -------------------
# Check & Send Reminder
# -------------------
st.subheader("🔔 Send Reminders Now")
if st.button("Check & Send Reminder"):
    if not user_phone:
        st.error("Please enter your phone number first!")
    else:
        now = datetime.now()
        reminders_sent = 0
        for med in st.session_state.medicines:
            if med["Hour"] == now.hour and med["Minute"] == now.minute:
                try:
                    message = client.messages.create(
                        body=f"⏰ Reminder: Time to take your medicine '{med['Medicine']}'",
                        from_=TWILIO_PHONE_NUMBER,
                        to=user_phone
                    )
                    st.success(f"Reminder sent for '{med['Medicine']}' ✅")
                    reminders_sent += 1
                except Exception as e:
                    st.error(f"Failed to send SMS: {e}")
        if reminders_sent == 0:
            st.info("No medicines scheduled for this time.")

















