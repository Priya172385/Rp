import streamlit as st
from textblob import TextBlob

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="🤖")
st.title("🤖 AI Sentiment Analyzer")
st.write("Enter any text and find out if it's Positive, Neutral, or Negative.")

# -----------------------------
# User input
# -----------------------------
user_text = st.text_area("Enter text here")

# -----------------------------
# Analyze sentiment
# -----------------------------
if st.button("Analyze Sentiment"):
    if user_text.strip() == "":
        st.error("Please enter some text to analyze!")
    else:
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity

        # Determine sentiment
        if polarity > 0:
            sentiment = "Positive 😄"
            st.success(f"Sentiment: {sentiment} (Polarity: {polarity:.2f})")
        elif polarity == 0:
            sentiment = "Neutral 😐"
            st.info(f"Sentiment: {sentiment} (Polarity: {polarity:.2f})")
        else:
            sentiment = "Negative 😢"
            st.error(f"Sentiment: {sentiment} (Polarity: {polarity:.2f})")







