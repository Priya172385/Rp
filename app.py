import streamlit as st
from datetime import date

st.title("🎂 Age Calculator")
dob = st.date_input("Select DOB")
today = date.today()
age = today.year - dob.year
st.success(f"You are {age} years old")
