import streamlit as st
st.title("📅 Daily Habit Tracker")
if "habits" not in st.session_state: st.session_state.habits=[]
habit = st.text_input("Add a habit")
if st.button("Add Habit"):
    if habit: st.session_state.habits.append(habit)
if st.session_state.habits:
    st.subheader("Your Habits")
    for h in st.session_state.habits: st.write("•", h)



