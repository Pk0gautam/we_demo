import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("food_app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS foods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    food_name TEXT,
    quantity INTEGER,
    total REAL,
    order_date TEXT
)
""")

conn.commit()

# Default Admin
cursor.execute(
    "INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)",
    ("admin", "admin123", "admin")
)
conn.commit()

# -----------------------------
# SESSION
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# FUNCTIONS
# -----------------------------
def login(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return cursor.fetchone()

def register(username, password):
    try:
        cursor.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username, password, "customer")
        )
        conn.commit()
        return True
    except:
        return False

# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.logged_in:

    st.title("🍔 Food Ordering System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login(user, pwd)

            if result:
                st.session_state.logged_in = True
                st.session_state.username = result[1]
                st.session_state.role = result[3]
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register(new_user, new_pwd):
                st.success("Registered Successfully")
            else:
                st.error("Username already exists")

# -----------------------------
# AFTER LOGIN
# -----------------------------
else:

    st.sidebar.success(
        f"{st.session_state.username} ({st.session_state.role})"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.cart = []
        st.rerun()

    # -------------------------
    # CUSTOMER
    # -------------------------
    if st.session_state.role == "customer":

        page = st.sidebar.selectbox(
            "Menu",
            ["Food Menu", "Cart", "My Orders"]
        )

        # FOOD MENU
        if page == "Food Menu":

            st.title("🍽 Food Menu")

            foods = pd.read_sql_query(
                "SELECT * FROM foods",
                conn
            )

            if foods.empty:
                st.warning("No food items available")

            for _, row in foods.iterrows():

                col1, col2 = st.columns([3,1])

                with col1:
                    st.subheader(row["name"])
                    st.write(f"₹{row['price']}")

                with col2:
                    qty = st.number_input(
                        f"Qty {row['id']}",
                        min_value=1,
                        value=1,
                        key=row["id"]
                    )

                    if st.button(
                        f"Add {row['name']}",
                        key=f"btn{row['id']}"
                    ):
                        st.session_state.cart.append({
                            "name": row["name"],
                            "price": row["price"],
                            "qty": qty
                        })

                        st.success("Added to Cart")

        # CART
        elif page == "Cart":

            st.title("🛒 Cart")

            total = 0

            if len(st.session_state.cart) == 0:
                st.info("Cart Empty")

            else:

                for item in st.session_state.cart:

                    subtotal = item["price"] * item["qty"]
                    total += subtotal

                    st.write(
                        f"{item['name']} x {item['qty']} = ₹{subtotal}"
                    )

                st.subheader(f"Total = ₹{total}")

                if st.button("Place Order"):

                    for item in st.session_state.cart:

                        cursor.execute("""
                        INSERT INTO orders(
                        username,
                        food_name,
                        quantity,
                        total,
                        order_date
                        )
                        VALUES(?,?,?,?,?)
                        """, (
                            st.session_state.username,
                            item["name"],
                            item["qty"],
                            item["price"] * item["qty"],
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        ))

                    conn.commit()

                    st.session_state.cart = []

                    st.success("Order Placed Successfully")

        # ORDERS
        elif page == "My Orders":

            st.title("📦 My Orders")

            query = """
            SELECT *
            FROM orders
            WHERE username=?
            """

            df = pd.read_sql_query(
                query,
                conn,
                params=(st.session_state.username,)
            )

            st.dataframe(df)

    # -------------------------
    # ADMIN
    # -------------------------
    elif st.session_state.role == "admin":

        page = st.sidebar.selectbox(
            "Admin Menu",
            [
                "Dashboard",
                "Add Food",
                "Manage Food",
                "View Orders"
            ]
        )

        # DASHBOARD
        if page == "Dashboard":

            st.title("📊 Dashboard")

            foods_count = pd.read_sql_query(
                "SELECT COUNT(*) c FROM foods",
                conn
            )["c"][0]

            orders_count = pd.read_sql_query(
                "SELECT COUNT(*) c FROM orders",
                conn
            )["c"][0]

            revenue = pd.read_sql_query(
                "SELECT SUM(total) t FROM orders",
                conn
            )["t"][0]

            if revenue is None:
                revenue = 0

            col1, col2, col3 = st.columns(3)

            col1.metric("Foods", foods_count)
            col2.metric("Orders", orders_count)
            col3.metric("Revenue ₹", revenue)

        # ADD FOOD
        elif page == "Add Food":

            st.title("➕ Add Food")

            name = st.text_input("Food Name")
            price = st.number_input(
                "Price",
                min_value=1.0
            )

            if st.button("Add Food"):

                cursor.execute(
                    "INSERT INTO foods(name,price) VALUES(?,?)",
                    (name, price)
                )

                conn.commit()

                st.success("Food Added")

        # MANAGE FOOD
        elif page == "Manage Food":

            st.title("🍔 Manage Food")

            df = pd.read_sql_query(
                "SELECT * FROM foods",
                conn
            )

            st.dataframe(df)

            delete_id = st.number_input(
                "Food ID to Delete",
                min_value=1
            )

            if st.button("Delete Food"):

                cursor.execute(
                    "DELETE FROM foods WHERE id=?",
                    (delete_id,)
                )

                conn.commit()

                st.success("Deleted")

        # VIEW ORDERS
        elif page == "View Orders":

            st.title("📦 All Orders")

            df = pd.read_sql_query(
                "SELECT * FROM orders",
                conn
            )

            st.dataframe(df)