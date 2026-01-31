import streamlit as st
st.title("🍲 Home Recipe Keeper")
if "recipes" not in st.session_state:
    st.session_state.recipes = []

recipe_name = st.text_input("Recipe Name")
ingredients = st.text_area("Ingredients (comma separated)")

if st.button("Add Recipe"):
    if recipe_name and ingredients:
        st.session_state.recipes.append({"Recipe": recipe_name, "Ingredients": ingredients})

st.subheader("Your Recipes")
for r in st.session_state.recipes:
    st.write(f"• {r['Recipe']}: {r['Ingredients']}")













