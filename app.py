import streamlit as st
from textblob import TextBlob
import pandas as pd

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="🤖")
st.title("🤖 AI Sentiment Analyzer with Bar Chart")
st.write("Enter text to find sentiment and visualize scores.")

# -----------------------------
# User input
# -----------------------------
user_text = st.text_area("Enter text here")

# -----------------------------
# Analyze sentiment
# -----------------------------
if st.button("Analyze Sentiment"):
    if user_text.strip() == "":
        st.error("Please enter some text!")
    else:
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity  # -1 to +1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1

        # Determine sentiment category
        if polarity > 0:
            sentiment = "Positive 😄"
        elif polarity == 0:
            sentiment = "Neutral 😐"
        else:
            sentiment = "Negative 😢"

        # Display sentiment
        st.subheader(f"Sentiment: {sentiment}")
        st.write(f"Polarity Score: {polarity:.2f}")
        st.write(f"Subjectivity Score: {subjectivity:.2f}")

        # -----------------------------
        # Bar chart of sentiment scores
        # -----------------------------
        sentiment_scores = {
            "Positive": max








