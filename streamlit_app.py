

import streamlit as st
import os
from MontysOOP.Employee import Employee
from MontysOOP.Menu import Menu
from MontysOOP.Coffee import Coffee
from datetime import datetime

# --- Helper Functions ---


def load_orders(emp_num):
    """
    Load and return the 5 most recent orders for the given employee number.
    """
    orders = []
    orders_path = os.path.join(
        os.path.dirname(__file__), 'MontysOOP', 'orders.txt')
    if not os.path.exists(orders_path):
        return []
    with open(orders_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 8:
                continue
            if str(parts[0]) == str(emp_num):
                # Parse timestamp for sorting
                try:
                    order_time = datetime.fromisoformat(parts[1])
                except Exception:
                    order_time = None
                orders.append({
                    'timestamp': order_time,
                    'coffee_type': parts[2],
                    'size': parts[3],
                    'milk': parts[4],
                    'flavor': parts[5],
                    'pump_level': parts[6],
                    'cost': parts[7],
                })
    # Sort by timestamp descending, take 5 most recent
    orders = sorted(
        [o for o in orders if o['timestamp']],
        key=lambda x: x['timestamp'], reverse=True
    )[:5]
    return orders


def save_order(order: Coffee):
    order.save()

# --- Streamlit App ---


st.set_page_config(
    page_title="Monty's Coffee OOP App",
    layout="centered"
)
st.sidebar.title("Monty's Coffee")
page = st.sidebar.radio(
    "Navigation",
    [
        "Login/Create User",
        "My Orders",
        "Place Order",
        "Update/Delete Order"
    ]
)

# --- Session State for User ---

if 'employee' not in st.session_state:
    st.session_state['employee'] = None


if page == "Login/Create User":
    st.header("Login or Create User")
    with st.form("user_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        extension = st.text_input("Phone Extension (4 digits)")
        emp_num = st.text_input(
            "Employee Number", help="This is your unique ID"
        )
        submitted = st.form_submit_button("Login/Create")
    if submitted:
        # Validation
        if not (
            fname and lname and extension.isdigit() and emp_num.isdigit()
        ):
            st.error("Please fill all fields with valid data.")
        else:
            st.session_state['employee'] = Employee(
                fname, lname, extension, int(emp_num)
            )
            st.success(
                f"Welcome, {fname} {lname}! Your employee number is {emp_num}."
            )


if st.session_state['employee']:
    emp = st.session_state['employee']
    emp_num = emp.get_emp_num()
    # Load menu
    menu_path = os.path.join(
        os.path.dirname(__file__), 'MontysOOP', 'menu.txt'
    )
    menu = Menu.from_file(menu_path)

    if page == "My Orders":
        st.header("Your 5 Most Recent Orders")
        orders = load_orders(emp_num)
        if not orders:
            st.info("No orders found.")
        else:
            for i, order in enumerate(orders, 1):
                order_time = (
                    order['timestamp'].strftime('%Y-%m-%d %I:%M %p')
                    if order['timestamp'] else 'Unknown'
                )
                with st.expander(f"Order #{i} - {order_time}"):
                    st.write(
                        f"**Coffee:** {order['size']} "
                        f"{order['coffee_type']}"
                    )
                    st.write(f"**Milk:** {order['milk']}")
                    st.write(
                        f"**Flavor:** {order['flavor']} "
                        f"({order['pump_level']})"
                    )
                    st.write(f"**Total:** ${order['cost']}")

    elif page == "Place Order":
        st.header("Place a New Order")
        if not menu:
            st.error("Menu could not be loaded.")
        else:
            with st.form("order_form"):
                coffee_type = st.selectbox("Coffee Type", menu.get_coffee())
                size = st.selectbox(
                    "Size", [s.split(':')[0].strip() for s in menu.get_prices()])
                milk = st.selectbox("Milk", menu.get_milks())
                flavor = st.selectbox("Flavor", menu.get_flavors())
                pump_level = "None"
                if flavor.lower() != "none":
                    pump_level = st.selectbox("Pump Level", menu.get_pumps())
                submit_order = st.form_submit_button("Place Order")
            if submit_order:
                # Create Coffee object and calculate cost
                order = Coffee(emp, coffee_type, size,
                               milk, flavor, pump_level)
                order.calculate_cost(menu)
                save_order(order)
                st.success("Order placed and saved!")

    elif page == "Update/Delete Order":
        st.header("Update or Delete Most Recent Order")
        orders = load_orders(emp_num)
        if not orders:
            st.info("No orders to update or delete.")
        else:
            most_recent = orders[0]
            st.subheader(
                f"Most Recent Order: {most_recent['timestamp'].strftime('%Y-%m-%d %I:%M %p') if most_recent['timestamp'] else 'Unknown'}")
            st.write(
                f"**Coffee:** {most_recent['size']} {most_recent['coffee_type']}")
            st.write(f"**Milk:** {most_recent['milk']}")
            st.write(
                f"**Flavor:** {most_recent['flavor']} ({most_recent['pump_level']})")
            st.write(f"**Total:** ${most_recent['cost']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Order"):
                    st.info(
                        "To update, please place a new order in the 'Place Order' tab. (Full update/delete logic can be added if desired.)")
            with col2:
                if st.button("Delete Order"):
                    # Delete logic: remove from file (not implemented yet)
                    st.warning("Delete functionality coming soon!")
else:
    if page != "Login/Create User":
        st.warning("Please login or create a user first.")
