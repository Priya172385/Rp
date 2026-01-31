import streamlit as st
import pandas as pd

st.set_page_config(page_title="Budget Planner", page_icon="💰")
st.title("💰 Personal Budget Planner")
st.write("Enter your income and expenses to see your budget balance.")

# Input Income
income = st.number_input("💵 Total Monthly Income", min_value=0.0, step=100.0)

# Input Expenses
st.subheader("📝 Enter Monthly Expenses")
expense_categories = ["Rent", "Food", "Transportation", "Utilities", "Entertainment", "Others"]
expenses = {}

for category in expense_categories:
    expenses[category] = st.number_input(f"{category} Expense", min_value=0.0, step=50.0)

# Calculate Total Expenses and Remaining Balance
if st.button("Calculate Budget"):
    total_expenses = sum(expenses.values())
    balance = income - total_expenses

    st.success(f"💸 Total Expenses: ${total_expenses:.2f}")
    st.success(f"💰 Remaining Balance: ${balance:.2f}")

    # Display Expenses Table
    df = pd.DataFrame(list(expenses.items()), columns=["Category", "Amount ($)"])
