import streamlit as st
st.title("😄 Emoji Mood Tracker")
mood = st.radio("How do you feel?", ["😀", "😐", "😢", "😡"])
st.write("Your mood today:", mood)
