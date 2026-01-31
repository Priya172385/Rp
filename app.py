import streamlit as st

st.title("💧 Water Intake Tracker")
if "water" not in st.session_state:
    st.session_state.water = 0

water_glass = st.number_input("Add glasses of water", 1, 10, 1)
if st.button("Add"):
    st.session_state.water += water_glass

st.subheader("Today's Water Intake")
st.write(f"You drank {st.session_state.water} glass(es) of water today! 🚰")












