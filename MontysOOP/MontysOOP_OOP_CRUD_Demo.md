# MontysOOP: Agentic Programming & OOP CRUD Demo (April 16, 2026)

This guide summarizes the steps taken today to refactor a procedural coffee ordering system into a fully Object-Oriented (OOP) and agentic workflow using Python. It demonstrates how to use agents (like Copilot) to iteratively build, debug, and enhance a project.

---

## 🟢 1. Project Setup
- Created a new folder: `MontysOOP/`
- Copied `menu.txt` into this folder for menu data.

## 🟢 2. OOP Class Creation
- **Menu.py**: Reads `menu.txt` and provides getter methods for coffee, prices, milks, flavors, and pumps.
- **Employee.py**: Represents an employee with private attributes, a `from_input` factory method, and a `__str__` method for display.
- **Coffee.py**: Represents a coffee order, encapsulates all order details, calculates cost (including pump upcharges), and saves orders to file.

## 🟢 3. Main Application Refactor
- **MontyOOP.py**:
  - Imports the OOP classes.
  - Main loop allows:
    - Creating an order (`Coffee.from_input`)
    - Printing a label/receipt
    - Confirming, updating, or deleting/cancelling the order before saving
    - Viewing, updating, and deleting orders in the current session (CRUD)
  - All file paths are robust (using `os.path`), so the app works from any directory.

## 🟢 4. Key Agentic Programming Steps
- Used Copilot/agent to:
  - Debug path issues (ensuring `menu.txt` and `orders.txt` are always found)
  - Refactor procedural code to OOP step by step
  - Add getter methods for encapsulation
  - Implement a full CRUD loop for orders
  - Annotate code for clarity and teaching

## 🟢 5. How to Run the Demo
```bash
cd MontysOOP
python MontyOOP.py
```

## 🟢 6. Teaching Notes
- Each class is annotated for students.
- The main loop demonstrates agentic, iterative improvement: ask, test, refactor, repeat.
- Students can extend this by adding persistent update/delete for orders in the file, or by adding more features.

---

*Generated with GitHub Copilot agentic programming workflow, April 16, 2026.*
