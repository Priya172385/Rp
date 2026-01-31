import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Average Calculator", page_icon="📊")

st.title("📊 Smart Average Calculator for Teachers")
st.write("Enter student marks to calculate total, average, and grade instantly.")

# Input
student_name = st.text_input("Student Name")

subjects = ["Maths", "Science", "English", "Computer", "Social"]
marks = {}

st.subheader("📝 Enter Marks")
for subject in subjects:
    marks[subject] = st.number_input(f"{subject} Marks", 0, 100, 0)

# Calculate
if st.button("Calculate Result"):
    total = sum(marks.values())
    average = total / len(subjects)

    # Grade logic
    if average >= 90:
        grade = "A+"
    elif average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "Fail"

    st.success(f"📌 Student: {student_name}")
    st.write(f"📚 Total Marks: **{total}**")
    st.write(f"📈 Average Marks: **{average:.2f}**")
    st.write(f"🏆 Grade: **{grade}**")

    # Display table
    df = pd.DataFrame(list(marks.items()), columns=["Subject", "Marks"])
    st.table(df)
