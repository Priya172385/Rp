import streamlit as st
st.title("🌤 Weather App")
city = st.text_input("Enter City Name")
if st.button("Get Weather"):
    st.write(f"Weather in {city}: Sunny, 25°C")  # placeholder


