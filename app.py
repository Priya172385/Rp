import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺")

st.title("🩺 AI Symptom Checker")
st.write("Enter your symptoms and let AI predict a possible condition.")
st.warning("⚠️ This is for educational purposes only. Not a medical diagnosis.")

# Sample training data
symptoms = [
    "fever cough headache",
    "sneezing runny nose cold",
    "chest pain shortness of breath",
    "stomach pain nausea vomiting",
    "fatigue body pain fever",
    "itching skin rash",
    "headache nausea sensitivity to light",
]

diseases = [
    "Flu",
    "Common Cold",
    "Heart Issue",
    "Food Poisoning",
    "Viral Infection",
    "Allergy",
    "Migraine"
]

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(symptoms)

model = MultinomialNB()
model.fit(X, diseases)

# User input
user_input = st.text_area("📝 Enter symptoms (comma or space separated)")

if st.button("Check Condition"):
    if user_input.strip() == "":
        st.error("Please enter symptoms.")
    else:
        user_vector = vectorizer.transform([user_input])
        prediction = model.predict(user_vector)[0]
        st.success(f"🧠 Possible Condition: **{prediction}**")
        st.info("Please consult a medical professional for accurate diagnosis.")
