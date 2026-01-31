import streamlit as st

st.title("🏠 Home Chores Tracker")
if "chores" not in st.session_state:
    st.session_state.chores = []

chore = st.text_input("Chore Name")
if st.button("Add Chore"):
    if chore:
        st.session_state.chores.append(chore)

st.subheader("Chore List")
for i, c in enumerate(st.session_state.chores, 1):
    st.write(f"{i}. {c}")











