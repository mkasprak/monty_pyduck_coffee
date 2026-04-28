# ☕ Monty's Coffee Order System

> *"Never give Merry the wrong milk again."*

A Python OOP teaching project built around **Monty PyDuck**, an intern in a universe of anthropomorphic ducks. After accidentally giving his boss **Merry McQuacken** a drink containing soy milk (she's severely allergic), Monty is tasked with building a proper coffee ordering system for the office.

---

## 🦆 The Story

| Character | Role |
|---|---|
| **Merry McQuacken** | Office manager. Oat milk only. Do NOT get this wrong. |
| **Monty PyDuck** | Intern. Responsible for the coffee run. Builds this app. |
| **Doug Mallardson** | Developer. Triple espresso, black. Always. |
| **Grace Gooseberg** | Accounting. Decaf soy latte — the ironic soy milk lover. |
| **Pip Pekinton** | New hire. Orders something different every day. |

---

## 🚀 How to Run Locally

```bash
# Install dependencies
pip install streamlit fpdf2

# Run the app
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
monty_pyduck_coffee/
├── streamlit_app.py          # Main Streamlit web app
├── README.md
└── MontysOOP/
    ├── Coffee.py             # Coffee class (OOP core)
    ├── Employee.py           # Employee class
    ├── Menu.py               # Menu class (reads menu.txt)
    ├── MontyOOP.py           # CLI version of the app
    ├── menu.txt              # Menu data file
    ├── orders.txt            # Saved orders (auto-created)
    └── passwords.txt         # User passwords (auto-created)
```

---

## 🗂️ App Pages

### 👤 Login / Create User
- Enter name, 4-digit extension, employee number, and password
- **New users** are created automatically on first login
- **Returning users** must enter their correct password

### 📋 My Orders
- View your 5 most recent orders with status (🕐 Pending / ✅ Filled)
- **🔁 Reorder This** — one click to reorder a past drink with all options pre-filled
- **☕ Order History** — bar chart of your most ordered drinks

### ☕ Place Order
- Choose coffee type, size, milk, flavor, and pump level from dropdown menus
- **Allergy warnings** appear on the verify screen for all allergen milks
- Must **acknowledge** the allergy warning before submitting
- Two-step flow: build order → verify → submit

### ✏️ Update / Delete Order
- View and manage your most recent order

### 🦆 Monty's Dashboard *(Intern Only)*
- Protected by PIN: **`quack`**
- See ALL orders from all employees
- Filter between pending and filled orders
- Each label shows: **employee name, extension, timestamp, allergy warnings**
- **📄 Download Label PDF** — generates a formatted PDF label for printing
- **✅ Mark as Filled** — removes order from the pending queue

---

## 🔒 orders.txt Format

Each line stores one order:

```
emp_num, timestamp, coffee_type, size, milk, flavor, pump_level, cost, status, fname, lname, extension
```

Status is either `Pending` or `Filled`.

---

## 🎓 OOP Concepts Demonstrated

| Concept | Where |
|---|---|
| Classes & Objects | `Coffee`, `Employee`, `Menu` |
| Private attributes (`__`) | All three classes |
| Getters & Setters | All three classes |
| `__str__` magic method | `Coffee`, `Employee` |
| `@classmethod` factory | `Employee.from_input()`, `Coffee.from_input()`, `Menu.from_file()` |
| File I/O (read/write/update) | `Coffee.save()`, `mark_order_filled()` |
| Dictionaries as lookup tables | `ALLERGY_WARNINGS` |
| Class reuse across interfaces | Same OOP classes used in CLI and web app |

---

## ⚠️ Allergy Warnings

| Milk | Allergen |
|---|---|
| Soy | Contains Soy |
| Oat | Contains Oats/Gluten |
| Coconut | Contains Tree Nuts |
| 2% | Contains Dairy |
| Whole | Contains Dairy |
| None | No allergens |

---

*Built with ❤️ (and a healthy fear of Merry McQuacken) using Python + Streamlit.*
