import streamlit as st
st.title("✍️ Word Counter")
text = st.text_area("Enter text")
if text:
    st.info(f"Words: {len(text.split())}")
