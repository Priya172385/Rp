import streamlit as st
import random

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Random Travel Destination Suggester",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Random Travel Destination Suggester")
st.write("Choose your preferred type of destination and get a random suggestion!")

# -----------------------------
# Destination data (categorized)
# -----------------------------
destinations = {
    "Beach": [
        {"name": "Bali", "country": "Indonesia", "image": "https://upload.wikimedia.org/wikipedia/commons/6/63/Pantai_Kuta_Bali.jpg"},
        {"name": "Maldives", "country": "Maldives", "image": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Maldives_beach.jpg"}
    ],
    "City": [
        {"name": "Paris", "country": "France", "image": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Paris_-_Eiffelturm_und_Marsfeld2.jpg"},
        {"name": "Tokyo", "country": "Japan", "image": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Tokyo_Tower_and_surrounding_buildings.jpg"},
        {"name": "New York", "country": "USA", "image": "https://upload.wikimedia.org/wikipedia/commons/4/47/Manhattan_skyline_from_Hudson_River.jpg"}
    ],
    "Adventure": [
        {"name": "Swiss Alps", "country": "Switzerland", "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Matterhorn_from_Domhütte_-_2.jpg"},
        {"name": "Patagonia", "country": "Argentina/Chile", "image": "https://upload.wikimedia.org/wikipedia/commons/b/b2/Glacier_Perito_Moreno_05.jpg"}
    ]
}

# -----------------------------
# User input: Filter type
# -----------------------------
destination_type = st.selectbox(
    "Select Type of Destination",
    ["Beach", "City", "Adventure"]
)

# -----------------------------
# Button to suggest a destination
# -----------------------------
if st.button("Suggest a Destination"):
    # Pick random destination from selected type
    suggestion = random.choice(destinations[destination_type])
    
    st.subheader(f"🌍 Your Random {destination_type} Destination:")
    st.markdown(f"**{suggestion['name']}, {suggestion['country']}**")
    
    # Display image if available
    st.image(suggestion["image"], use_column_width=True)

# -----------------------------
# Optional: Show all destinations table
# -----------------------------
if st.checkbox("Show all destinations"):
    all_data = []
    for category, places in destinations.items():
        for p in places:
            all_data.append({"Type": category, "Name": p["name"], "Country": p["country"]})
    st.subheader("📋 All Destinations")
    st.dataframe(all_data)






