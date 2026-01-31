import streamlit as st, random
st.title("🐾 Random Animal Fact")
facts = [
    "A group of flamingos is called a 'flamboyance'.",
    "Sloths can hold their breath longer than dolphins.",
    "Butterflies can taste with their feet."
]
if st.button("Show Fact"):
    st.write(random.choice(facts))




