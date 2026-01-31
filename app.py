import streamlit as st
symptoms = st.text_area("Enter Symptoms")
if st.button("Predict Disease"):
    st.write("Possible Disease: Flu / Cold / Migraine")  # simple placeholder
