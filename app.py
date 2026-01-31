import streamlit as st
from datetime import datetime, time
import pandas as pd
import time as t
import base64

st.title("💊 Medicine Reminder with Notifications")

# Initialize session state
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# Add medicine form
with st.form("medicine_form"):
    med_name = st.text_input("Medicine Name")
    med_time = st.time_input("Time to Take Medicine")
    submitted = st.form_submit_button("Add Medicine")
    if submitted:
        st.session_state.medicines.append({"Medicine": med_name, "Time": med_time})
        st.success(f"Medicine {med_name} added at {med_time}!")

# Show medicine schedule
if st.session_state.medicines:
    st.subheader("🗓️ Medicine Schedule")
    df = pd.DataFrame(st.session_state.medicines)
    st.dataframe(df)

    # Real-time notifications
    st.subheader("🔔 Notifications")
    now = datetime.now().time()
    notified = False
    for med in st.session_state.medicines:
        # If current time matches medicine time (within 1 min)
        med_t = med["Time"]
        if med_t.hour == now.hour and med_t.minute == now.minute:
            st.warning(f"⏰ Time to take your medicine: {med['Medicine']}!")
            notified = True

    if not notified:
        st.info("No medicine due right now.")















