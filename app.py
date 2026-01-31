import streamlit as st

st.title("💊 Medicine Reminder")
if "medicines" not in st.session_state:
    st.session_state.medicines = []

name = st.text_input("Medicine Name")
time = st.time_input("Time to Take")
if st.button("Add Medicine"):
    st.session_state.medicines.append({"Medicine": name, "Time": str(time)})
    st.success(f"Medicine {name} added!")

if st.session_state.medicines:
    st.subheader("Medicine Schedule")
    for med in st.session_state.medicines:
        st.write(f"{med['Medicine']} - {med['Time']}")














