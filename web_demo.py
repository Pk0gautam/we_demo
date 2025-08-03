import streamlit as st

# Page config
st.set_page_config(page_title="Food Menu", layout="wide")

# App Title
st.title("🍽️ Welcome to Foodie's Paradise")

# Create top navbar using tabs
tabs = st.tabs(["🏠 Home", "🔐 Sign In", "📝 Sign Up", "🛍️ Order", "🛒 Cart"])

# Sample food data
food_items = [
    {
        "name": "Pancakes",
        "type": "Breakfast",
        "description": "Fluffy pancakes served with maple syrup and berries.",
        "image": "https://cdn.pixabay.com/photo/2017/05/07/08/56/pancakes-2291908_960_720.jpg"
    },
    {
        "name": "Chai",
        "type": "Breakfast",
        "description": "Fluffy pancakes served with maple syrup and berries./price FREE",
        "image": "https://c.ndtvimg.com/2023-01/ai6hl0gg_masala-chai_625x300_17_January_23.jpg?im=FaceCrop,algorithm=dnn,width=1200,height=675.jpg"
    },
    {
        "name": "sandwich",
        "type": "Breakfast",
        "description": "Fluffy pancakes served with maple syrup and berries./price FREE",
        "image": "https://www.southernliving.com/thmb/UW4kKKL-_M3WgP7pkL6Pb6lwcgM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Ham_Sandwich_011-1-49227336bc074513aaf8fdbde440eafe.jpg"
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

# --------- Tab 1: Home ---------
with tabs[0]:
    st.subheader("🍴 Explore Our Menu")
    meal_type = st.radio("Filter by Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Dessert"], horizontal=True)

    if meal_type != "All":
        filtered_items = [item for item in food_items if item["type"] == meal_type]
    else:
        filtered_items = food_items

    cols = st.columns(2)
    for i, item in enumerate(filtered_items):
        with cols[i % 2]:
            st.image(item["image"], width=350)
            st.subheader(item["name"])
            st.write(item["description"])
            st.caption(f"🍴 {item['type']}")

# --------- Tab 2: Sign In ---------
with tabs[1]:
    st.subheader("🔐 Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        st.success(f"Welcome back, {username}!")

# --------- Tab 3: Sign Up ---------
with tabs[2]:
    st.subheader("📝 Sign Up")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Create Account"):
        if new_password == confirm_password:
            st.success("Account created successfully!")
        else:
            st.error("Passwords do not match.")

# --------- Tab 4: Order ---------
with tabs[3]:
    st.subheader("🛍️ Place Your Order")
    selected_food = st.selectbox("Select an item", [item["name"] for item in food_items])
    quantity = st.number_input("Quantity", min_value=1, value=1)
    if st.button("Submit Order"):
        st.success(f"Order placed for {quantity} x {selected_food}!")

# --------- Tab 5: Cart ---------
with tabs[4]:
    st.subheader("🛒 Your Cart")
    st.info("Go back nothing will be added to cart 😅😅😅")

# Footer
st.markdown("---")
st.markdown("© 2025 Foodie's Paradise | Powered by Streamlit")
