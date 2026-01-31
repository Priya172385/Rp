import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calorie Intake Tracker", page_icon="🍎")
st.title("🍎 Calorie Intake Tracker")
st.write("Track your daily calorie intake and monitor your diet.")

# Input daily calorie goal
calorie_goal = st.number_input("Daily Calorie Goal", min_value=0, step=100)

# Session state to store meals
if "meals" not in st.session_state:
    st.session_state.meals = []

st.subheader("➕ Add Meal")
meal_name = st.text_input("Meal Name")
meal_calories = st.number_input("Calories", min_value=0, step=50)

if st.button("Add Meal"):
    if meal_name.strip() == "":
        st.error("Please enter meal name")
    else:
        st.session_state.meals.append({"Meal": meal_name, "Calories": meal_calories})
        st.success(f"Added {meal_name} ({meal_calories} kcal)")

# Display meal table
if st.session_state.meals:
    st.subheader("📋 Meals Logged Today")
    df = pd.DataFrame(st.session_state.meals)
    st.dataframe(df)

    total_calories = df_

