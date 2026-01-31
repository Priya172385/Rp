import streamlit as st

st.title("📝 Grocery List Manager")
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

item = st.text_input("Add Item to Grocery List")
if st.button("Add Item"):
    if item:
        st.session_state.grocery_list.append(item)

st.subheader("Your Grocery List:")
for i, itm in enumerate(st.session_state.grocery_list, 1):
    st.write(f"{i}. {itm}")










