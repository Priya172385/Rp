import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Leave Tracker", page_icon="🏢")

st.title("🏢 Employee Leave Balance Tracker")
st.write("Employees can easily check their remaining leave balance.")

# Session state to store employee data
if "employees" not in st.session_state:
    st.session_state.employees = []

st.subheader("➕ Add Employee Leave Details")

emp_id = st.text_input("Employee ID")
emp_name = st.text_input("Employee Name")

total_leave = st.number_input("Total Leave Allowed", min_value=0, step=1)
used_leave = st.number_input("Leave Used", min_value=0, step=1)

if st.button("Add / Update Employee"):
    if emp_name == "" or emp_id == "":
        st.error("Please enter Employee ID and Name")
    elif used_leave > total_leave:
        st.error("Used leave cannot be greater than total leave")
    else:
        remaining_leave = total_leave - used_leave

        # Update if employee exists
        updated = False
        for emp in st.session_state.employees:
            if emp["ID"] == emp_id:
                emp["Name"] = emp_name
                emp["Total Leave"] = total_leave
                emp["Used Leave"] = used_leave
                emp["Remaining Leave"] = remaining_leave
                updated = True
