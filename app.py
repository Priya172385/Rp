import streamlit as st
from twilio.rest import Client
from datetime import datetime
import pandas as pd

st.title("💊 Medicine Reminder with Phone SMS Notification")

# Twilio Credentials (replace with your own)
TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"  # Twilio phone number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# User's phone number
user_phone = st.text_input("Enter your phone number (with country code, e.g., +911234567890)")

# Initialize medicines list
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# Add medicine form
with st.form("medicine_form"):
    med_name = st.text_input("Medicine Name")
    med_hour = st.number_input("Hour to take medicine (0-23)", 0, 23)
    med_minute = st.number_input("Minute to take medicine (0-59)", 0, 59)
    submitted = st.form_submit_button("Add Medicine")
    if submitted:
        st.session_state.medicines.append({
            "Medicine": med_name,
            "Hour": med_hour,
            "Minute": med_minute
        })
        st.success(f"Medicine {med_name} added at {med_hour:02d}:{med_minute:02d}!")

# Show medicine schedule
if st.session_state.medicines:
    st.subheader("🗓️ Medicine Schedule")
    df = pd.DataFrame(st.session_state.medicines)
    st.dataframe(df)

# Check for medicine time and send SMS
if st.button("Check & Send Reminder"):
    if not user_phone:
        st.error("Please enter your phone number first!")
    else:
        now = datetime.now()
        reminders_sent = 0
        for med in st.session_state.medicines:
            if med["Hour"] == now.hour and med["Minute"] == now.minute:
                # Send SMS
                message = client.messages.create(
                    body=f"⏰ Reminder: Time to take your medicine '{med['Medicine']}'",
                    from_=TWILIO_PHONE_NUMBER,
                    to=user_phone
                )
                st.success(f"Reminder sent for {med['Medicine']} ✅")
                reminders_sent += 1
        if reminders_sent == 0:
            st.info("No medicines scheduled for this time.")
















