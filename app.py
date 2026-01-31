import streamlit as st, random
st.title("❤️ Love Calculator")
name1 = st.text_input("Your name")
name2 = st.text_input("Partner name")
if st.button("Calculate Love"):
    st.success(f"Love Score: {random.randint(50,100)}% 💘")
