import streamlit as st
import random

st.set_page_config(page_title="Mood Quotes", page_icon="✨")

st.title("✨ Mood-Based Quote Generator")

st.write("How are you feeling today?")

quotes = {
    "Happy 😊": [
        "Happiness is a journey, not a destination.",
        "Smile — it looks good on you!",
        "Joy is contagious, spread it."
    ],
    "Motivated 💪": [
        "Push yourself, no one else will.",
        "Dream big. Start small. Act now.",
        "Success is built one step at a time."
    ],
    "Calm 🌿": [
        "Breathe in peace, breathe out stress.",
        "Slow down — you’re doing fine.",
        "Stillness is powerful."
    ]
}

mood = st.selectbox("Select your mood", quotes.keys())

if st.button("✨ Show Quote"):
    st.success(random.choice(quotes[mood]))
