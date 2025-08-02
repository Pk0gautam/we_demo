import streamlit as st

# Page configuration
st.set_page_config(page_title="Food Menu", layout="wide")

# App title
st.title("🍽️ Welcome to Foodie's Paradise")

# Sidebar Filters
st.sidebar.header("Filter Menu")
meal_type = st.sidebar.radio("Select Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Dessert"])

# Sample food data
food_items = [
    {
        "name": "Pancakes",
        "type": "Breakfast",
        "description": "Fluffy pancakes served with maple syrup and berries.",
        "image": "https://cdn.pixabay.com/photo/2017/05/07/08/56/pancakes-2291908_960_720.jpg"
    },
    {
        "name": "Caesar Salad",
        "type": "Lunch",
        "description": "Classic Caesar salad with romaine, croutons, and parmesan.",
        "image": "https://www.jonesdairyfarm.com/wp-content/uploads/2024/10/Bacon-Caesar-Salad-1024x683.jpg"
    },
    {
        "name": "Spaghetti Bolognese",
        "type": "Dinner",
        "description": "Traditional Italian pasta with meat sauce.",
        "image": "https://img.chefkoch-cdn.de/rezepte/393031127655461/bilder/1585337/crop-960x540/spaghetti-bolognese.jpg"
    },
    {
        "name": "Chocolate Cake",
        "type": "Dessert",
        "description": "Rich chocolate cake with fudge frosting.",
        "image": "https://www.hersheyland.com/content/dam/hersheyland/en-us/recipes/recipe-images/2-hersheys-perfectly-chocolate-chocolate-cake-recipe-hero.jpg.jpg"
    },
]

# Filter food items
if meal_type != "All":
    filtered_items = [item for item in food_items if item["type"] == meal_type]
else:
    filtered_items = food_items

# Display food items
cols = st.columns(2)
for i, item in enumerate(filtered_items):
    with cols[i % 2]:
        st.image(item["image"], width=350)
        st.subheader(item["name"])
        st.write(item["description"])
        st.caption(f"🍴 {item['type']}")

# Footer
st.markdown("---")
st.markdown("© 2025 Foodie's Paradise | Powered by Streamlit")
