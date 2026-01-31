import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

st.set_page_config(page_title="Fake News Detector", page_icon="📰")
st.title("📰 Fake News Detector")
st.write("Enter a news headline or text to check if it's Fake or Real news.")

# Sample training data (for demo purposes)
data = {
    'text': [
        "NASA confirms water on Mars",
        "Aliens spotted in New York",
        "Stock markets reach all-time high",
        "Politician wins election with 99% votes",
        "New study shows chocolate is healthy",
        "Celebrity marries alien from outer space",
        "COVID vaccines approved by WHO",
        "Man travels through time using machine",
    ],
    'label': [
        "Real",
        "Fake",
        "Real",
        "Fake",
        "Real",
        "Fake",
        "Real",
        "Fake",
    ]
}

df = pd.DataFrame(data)

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df[']()
