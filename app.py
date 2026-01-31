import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Average Calculator", page_icon="📊")

st.title("📊 Student Marks & Average Automation")
st.write("Teachers can enter marks for all students and get instant averages.")

subjects = ["Maths", "Science", "English", "Computer", "Social"]

num_students = st.number_input("Enter number of students", min_value=1, step=1)

students_data = []

st.subheader("📝 Enter Student Marks")

for i in range(int(num_students)):
    st.markdown(f"### Student {i+1}")
    name = st.text_input(f"Student Name {i+1}", key=f"name{i}")

    marks = []
    for subject in subjects:
        mark = st.number_input(
            f"{subject} Marks",
            min_value=0,
            max_value=100,
            key=f"{subject}{i}"
        )
        marks.append(mark)

    total = sum(marks)
    average = total / len(subjects)

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

    students_data.append([
        name, total, round(average, 2), grade
    ])

# Display result
if st.button("📈 Calculate Results"):
    df = pd.DataFrame(
        students_data,
        columns=["Student Name", "Total Marks", "Average", "Grade"]
    )
    st.success("✅ Results Calculated Successfully!")
    st.dataframe(df)
