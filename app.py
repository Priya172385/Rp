import streamlit as st
from textblob import TextBlob
import pandas as pd

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="🤖")
st.title("🤖 AI Sentiment Analyzer with Bar Chart")
st.write("Type any text below to analyze sentiment and see a bar chart visualization.")

# -----------------------------
# User input
# -----------------------------
user_text = st.text_area("Enter your text here:")

# -----------------------------
# Analyze sentiment
# -----------------------------
if st.button("Analyze Sentiment"):
    # Check if input is empty
    if user_text.strip() == "":
        st.error("Please enter some text to analyze!")
    else:
        # Use TextBlob to get polarity (-1 to 1) and subjectivity (0 to 1)
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob









