

import streamlit as st
import os
from datetime import datetime, date
import zoneinfo
from fpdf import FPDF
from MontysOOP.Coffee import Coffee
from MontysOOP.Menu import Menu
from MontysOOP.Employee import Employee

# --- Helper Functions ---


def format_central(dt):
    """Format datetime in Central Time as 'Month day year, hh:mm AM/PM'"""
    if not dt:
        return 'Unknown'
    try:
        central = dt.astimezone(zoneinfo.ZoneInfo('America/Chicago'))
    except Exception:
        central = dt
    return central.strftime('%B %d %Y, %I:%M %p')


def load_orders(emp_num):
    """
    Load and return the 5 most recent orders for the given employee.
    Supports both old (8-field) and new (12-field) order formats.
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
                try:
                    order_time = datetime.fromisoformat(parts[1])
                    if order_time.tzinfo is None:
                        order_time = order_time.replace(
                            tzinfo=zoneinfo.ZoneInfo('America/Chicago'))
                    else:
                        order_time = order_time.astimezone(
                            zoneinfo.ZoneInfo('America/Chicago'))
                except Exception:
                    order_time = None
                orders.append({
                    'timestamp': order_time,
                    'timestamp_raw': parts[1],
                    'coffee_type': parts[2],
                    'size': parts[3],
                    'milk': parts[4],
                    'flavor': parts[5],
                    'pump_level': parts[6],
                    'cost': parts[7],
                    'status': parts[8] if len(parts) > 8 else 'Pending',
                    'fname': parts[9] if len(parts) > 9 else '',
                    'lname': parts[10] if len(parts) > 10 else '',
                    'extension': parts[11] if len(parts) > 11 else '',
                })
    orders = sorted(
        [o for o in orders if o['timestamp']],
        key=lambda x: x['timestamp'], reverse=True
    )[:5]
    return orders


def save_order(order: Coffee):
    order.save()


def mark_order_filled(emp_num_str, timestamp_raw):
    """
    Rewrite orders.txt updating the matching order's status to 'Filled'.
    Matches on emp_num + raw ISO timestamp string.
    """
    orders_path = os.path.join(
        os.path.dirname(__file__), 'MontysOOP', 'orders.txt')
    if not os.path.exists(orders_path):
        return False
    lines = []
    found = False
    with open(orders_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if (
                len(parts) >= 2
                and parts[0] == emp_num_str
                and parts[1] == timestamp_raw
            ):
                if len(parts) > 8:
                    parts[8] = 'Filled'
                else:
                    parts.append('Filled')
                lines.append(','.join(parts) + '\n')
                found = True
            else:
                lines.append(
                    line if line.endswith('\n') else line + '\n'
                )
    if found:
        with open(orders_path, 'w') as f:
            f.writelines(lines)
    return found


def generate_label_pdf(order):
    """Generate a PDF label for an order using fpdf2. Returns bytes."""
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "MONTY'S COFFEE", ln=True, align='C')
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, "ORDER LABEL", ln=True, align='C')
    pdf.ln(3)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    # Employee info
    fname = order.get('fname', '')
    lname = order.get('lname', '')
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Employee: {fname} {lname}", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(
        0, 7,
        f"Emp #: {order['emp_num']}  |  Ext: "
        f"{order.get('extension', 'N/A')}",
        ln=True
    )
    order_time = format_central(order['timestamp'])
    pdf.cell(0, 7, f"Time: {order_time}", ln=True)
    status = order.get('status', 'Pending')
    pdf.cell(0, 7, f"Status: {status}", ln=True)
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    # Order details
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0, 9,
        f"{order['size']} {order['coffee_type']}",
        ln=True
    )
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 7, f"Milk:   {order['milk']}", ln=True)
    pdf.cell(
        0, 7,
        f"Flavor: {order['flavor']} ({order['pump_level']})",
        ln=True
    )
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, f"TOTAL: ${order['cost']}", ln=True)
    # Allergy warning
    allergy = ALLERGY_WARNINGS.get(order['milk'], '')
    if allergy:
        pdf.ln(3)
        plain = allergy.replace('**', '').replace('⚠️ ', 'WARNING: ')
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(200, 0, 0)
        pdf.multi_cell(0, 7, plain)
        pdf.set_text_color(0, 0, 0)
    return bytes(pdf.output())


def get_passwords_path():
    """Return the path to the passwords file."""
    return os.path.join(
        os.path.dirname(__file__), 'MontysOOP', 'passwords.txt'
    )


def load_passwords():
    """Load passwords dict {emp_num_str: password} from passwords.txt."""
    passwords = {}
    path = get_passwords_path()
    if not os.path.exists(path):
        return passwords
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split(',', 1)
            if len(parts) == 2:
                passwords[parts[0]] = parts[1]
    return passwords


def save_password(emp_num, password):
    """Append a new emp_num,password entry to passwords.txt."""
    path = get_passwords_path()
    with open(path, 'a') as f:
        f.write(f"{emp_num},{password}\n")


def load_all_orders():
    """Load ALL orders from orders.txt for Monty's Dashboard."""
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
            try:
                order_time = datetime.fromisoformat(parts[1])
                if order_time.tzinfo is None:
                    order_time = order_time.replace(
                        tzinfo=zoneinfo.ZoneInfo('America/Chicago'))
                else:
                    order_time = order_time.astimezone(
                        zoneinfo.ZoneInfo('America/Chicago'))
            except Exception:
                order_time = None
            orders.append({
                'emp_num': parts[0],
                'timestamp': order_time,
                'timestamp_raw': parts[1],
                'coffee_type': parts[2],
                'size': parts[3],
                'milk': parts[4],
                'flavor': parts[5],
                'pump_level': parts[6],
                'cost': parts[7],
                'status': parts[8] if len(parts) > 8 else 'Pending',
                'fname': parts[9] if len(parts) > 9 else '',
                'lname': parts[10] if len(parts) > 10 else '',
                'extension': parts[11] if len(parts) > 11 else '',
            })
    return sorted(
        [o for o in orders if o['timestamp']],
        key=lambda x: x['timestamp'], reverse=True
    )

# --- Streamlit App ---


# --- Allergy Warnings ---
# Maps each milk option to its allergen warning message.
ALLERGY_WARNINGS = {
    "Soy":     "⚠️ This drink contains **Soy**. May cause reactions in those with soy allergies.",
    "Oat":     "⚠️ This drink contains **Oats/Gluten**. May cause reactions in those with gluten sensitivities.",
    "Coconut": "⚠️ This drink contains **Coconut (Tree Nut)**. May cause reactions in those with tree nut allergies.",
    "2%":      "⚠️ This drink contains **Dairy**. May cause reactions in those with lactose intolerance or dairy allergies.",
    "Whole":   "⚠️ This drink contains **Dairy**. May cause reactions in those with lactose intolerance or dairy allergies.",
}

st.set_page_config(
    page_title="Monty's Coffee OOP App",
    layout="centered"
)

# --- Dark Mode Toggle ---
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False
st.session_state['dark_mode'] = st.sidebar.checkbox(
    "🌙 Dark Mode", value=st.session_state['dark_mode']
)
if st.session_state['dark_mode']:
    st.markdown("""
    <style>
    .stApp { background-color: #1e1e2e !important; color: #cdd6f4 !important; }
    section[data-testid="stSidebar"] { background-color: #181825 !important; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #313244 !important; color: #cdd6f4 !important; }
    .stExpander { background-color: #27273a !important; }
    .stAlert { background-color: #313244 !important; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Monty's Coffee")
page = st.sidebar.radio(
    "Navigation",
    [
        "Login/Create User",
        "My Orders",
        "Place Order",
        "Update/Delete Order",
        "🦆 Monty's Dashboard"
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
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login / Create Account")
    if submitted:
        # Validation
        if not (
            fname and lname
            and extension.isdigit() and len(extension) == 4
            and emp_num.isdigit()
            and password
        ):
            st.error(
                "Please fill all fields. "
                "Extension must be exactly 4 digits."
            )
        else:
            passwords = load_passwords()
            emp_key = emp_num.strip()
            if emp_key in passwords:
                # Returning user — verify password
                if passwords[emp_key] == password:
                    st.session_state['employee'] = Employee(
                        fname, lname, extension, int(emp_num)
                    )
                    st.success(
                        f"Welcome back, {fname} {lname}! 👋"
                    )
                else:
                    st.error(
                        "Incorrect password. Please try again."
                    )
            else:
                # New user — create account and save password
                save_password(emp_key, password)
                st.session_state['employee'] = Employee(
                    fname, lname, extension, int(emp_num)
                )
                st.success(
                    f"Account created! Welcome, {fname} {lname}! 🎉"
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
                order_time = format_central(order['timestamp'])
                status = order.get('status', 'Pending')
                status_icon = "✅" if status == "Filled" else "🕐"
                with st.expander(
                    f"Order #{i} — {order_time} "
                    f"{status_icon} {status}"
                ):
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
                    if st.button("🔁 Reorder This", key=f"reorder_{i}"):
                        st.session_state['order_form_data'] = {
                            'coffee_type': order['coffee_type'],
                            'size': order['size'],
                            'milk': order['milk'],
                            'flavor': order['flavor'],
                            'pump_level': order['pump_level'],
                        }
                        st.session_state['order_verification'] = True
                        st.session_state['page_override'] = "Place Order"
                        st.rerun()

            # --- Order History Chart ---
            st.subheader("☕ Your Order History")
            counts = {}
            for o in orders:
                key = o['coffee_type']
                counts[key] = counts.get(key, 0) + 1
            st.bar_chart(counts)

    elif page == "Place Order":
        st.header("Place a New Order")
        if not menu:
            st.error("Menu could not be loaded.")
        else:
            # Step 1: Gather order details
            if 'order_form_data' not in st.session_state:
                st.session_state['order_form_data'] = None
            if 'order_verification' not in st.session_state:
                st.session_state['order_verification'] = False

            if not st.session_state['order_verification']:
                # Pre-populate dropdowns if coming from Reorder
                prev = st.session_state.get('order_form_data') or {}
                coffee_opts = menu.get_coffee()
                size_opts = [
                    s.split(':')[0].strip()
                    for s in menu.get_prices()
                ]
                milk_opts = menu.get_milks()
                flavor_opts = menu.get_flavors()
                pump_opts = menu.get_pumps()

                def _idx(lst, val):
                    return lst.index(val) if val in lst else 0

                with st.form("order_form"):
                    coffee_type = st.selectbox(
                        "Coffee Type", coffee_opts,
                        index=_idx(coffee_opts, prev.get('coffee_type'))
                    )
                    size = st.selectbox(
                        "Size", size_opts,
                        index=_idx(size_opts, prev.get('size'))
                    )
                    milk = st.selectbox(
                        "Milk", milk_opts,
                        index=_idx(milk_opts, prev.get('milk'))
                    )
                    flavor = st.selectbox(
                        "Flavor", flavor_opts,
                        index=_idx(flavor_opts, prev.get('flavor'))
                    )
                    pump_level = "None"
                    if flavor.lower() != "none":
                        pump_level = st.selectbox(
                            "Pump Level", pump_opts,
                            index=_idx(pump_opts, prev.get('pump_level'))
                        )
                    submit_order = st.form_submit_button(
                        "Next: Verify Order"
                    )
                if submit_order:
                    st.session_state['order_form_data'] = {
                        'coffee_type': coffee_type,
                        'size': size,
                        'milk': milk,
                        'flavor': flavor,
                        'pump_level': pump_level
                    }
                    st.session_state['order_verification'] = True

            # Step 2: Show verification and ask for confirmation
            if st.session_state['order_verification']:
                data = st.session_state['order_form_data']
                # Create Coffee object for preview (with current Central time)
                now_central = datetime.now(
                    zoneinfo.ZoneInfo('America/Chicago'))
                preview_order = Coffee(
                    emp,
                    data['coffee_type'],
                    data['size'],
                    data['milk'],
                    data['flavor'],
                    data['pump_level']
                )
                preview_order._Coffee__timestamp = now_central  # force timestamp
                preview_order.calculate_cost(menu)
                st.subheader("Verify Your Order")
                st.write(f"**Coffee:** {data['size']} {data['coffee_type']}")
                st.write(f"**Milk:** {data['milk']}")
                st.write(
                    f"**Flavor:** {data['flavor']} ({data['pump_level']})")
                st.write(f"**Total:** ${preview_order.get_cost():.2f}")
                st.write(f"**Order Time:** {format_central(now_central)}")

                # --- Allergy Warning ---
                allergy_msg = ALLERGY_WARNINGS.get(data['milk'])
                if allergy_msg:
                    st.warning(allergy_msg)
                    allergy_confirmed = st.checkbox(
                        "I understand and confirm this milk selection."
                    )
                else:
                    # No dairy/allergen milk selected (e.g., "None")
                    allergy_confirmed = True

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(
                        "Submit Order", disabled=not allergy_confirmed
                    ):
                        # Actually save order with forced Central time
                        preview_order.set_cost(preview_order.get_cost())
                        preview_order.save()
                        st.success("Order placed and saved!")
                        st.session_state['order_verification'] = False
                        st.session_state['order_form_data'] = None
                with col2:
                    if st.button("Make Changes"):
                        st.session_state['order_verification'] = False
                with col3:
                    if st.button("Cancel Order"):
                        st.session_state['order_verification'] = False
                        st.session_state['order_form_data'] = None

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

    elif page == "🦆 Monty's Dashboard":
        st.header("🦆 Monty's Dashboard — All Orders")
        st.caption("Intern view: see all orders and print/download labels.")
        intern_pin = st.text_input(
            "Enter Intern PIN to access dashboard",
            type="password"
        )
        if intern_pin == "quack":
            all_orders = load_all_orders()
            if not all_orders:
                st.info("No orders found yet.")
            else:
                pending = [
                    o for o in all_orders if o.get('status') != 'Filled'
                ]
                filled = [
                    o for o in all_orders if o.get('status') == 'Filled'
                ]
                st.success(
                    f"📋 {len(pending)} pending  |  "
                    f"✅ {len(filled)} filled  |  "
                    f"Total: {len(all_orders)}"
                )
                show_filled = st.checkbox("Show filled orders too")
                display_orders = (
                    all_orders if show_filled else pending
                )
                for i, order in enumerate(display_orders, 1):
                    order_time = format_central(order['timestamp'])
                    allergy = ALLERGY_WARNINGS.get(order['milk'], "")
                    status = order.get('status', 'Pending')
                    status_icon = "✅" if status == "Filled" else "🕐"
                    fname = order.get('fname', '')
                    lname = order.get('lname', '')
                    ext = order.get('extension', '')
                    header = (
                        f"🏷️ #{i} | {fname} {lname} "
                        f"(Ext: {ext}) | {order_time} "
                        f"| {status_icon} {status}"
                    )
                    with st.expander(header):
                        st.write(
                            f"**Employee:** {fname} {lname}  "
                            f"| Emp #: {order['emp_num']}  "
                            f"| Ext: {ext}"
                        )
                        st.write(f"**Time:** {order_time}")
                        st.write(
                            f"**Coffee:** {order['size']} "
                            f"{order['coffee_type']}"
                        )
                        st.write(f"**Milk:** {order['milk']}")
                        if allergy:
                            st.warning(allergy)
                        st.write(
                            f"**Flavor:** {order['flavor']} "
                            f"({order['pump_level']})"
                        )
                        st.write(f"**Total:** ${order['cost']}")
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            # PDF Download
                            pdf_bytes = generate_label_pdf(order)
                            st.download_button(
                                label="📄 Download Label PDF",
                                data=pdf_bytes,
                                file_name=(
                                    f"label_{order['emp_num']}_"
                                    f"{i}.pdf"
                                ),
                                mime="application/pdf",
                                key=f"pdf_{i}"
                            )
                        with btn_col2:
                            # Mark as Filled
                            if status != 'Filled':
                                if st.button(
                                    "✅ Mark as Filled",
                                    key=f"fill_{i}"
                                ):
                                    mark_order_filled(
                                        order['emp_num'],
                                        order['timestamp_raw']
                                    )
                                    st.success("Order marked as filled!")
                                    st.rerun()
                            else:
                                st.write("✅ Already filled")
        elif intern_pin:
            st.error("Incorrect PIN. Access denied! 🦆")
else:
    if page != "Login/Create User":
        st.warning("Please login or create a user first.")
