"""
    creating the coffee class
"""

#  importing the other classes we will need
import os
from datetime import datetime
from Employee import Employee
from Menu import Menu


class Coffee:
    # ☕ The __init__ method is the constructor for our class.
    # It's called when we create a new Coffee object.
    # We've added the employee who is ordering and a timestamp.
    def __init__(
        self, employee, coffee_type, size, milk, flavor, pump_level
    ):
        # --- Private Attributes 🔐 ---
        self.__employee = employee  # The Employee object
        # Automatically set to the current time
        self.__timestamp = datetime.now()
        self.__coffee_type = coffee_type
        self.__size = size
        self.__milk = milk
        self.__flavor = flavor
        self.__pump_level = pump_level  # e.g., "Light", "Normal", "Heavy"
        self.__cost = 0.0  # Cost is calculated *after* creation.

    # --- Getters 📥 ---
    # These methods safely get the values of our private attributes.
    def get_employee(self):
        return self.__employee

    def get_timestamp(self):
        return self.__timestamp

    def get_coffee_type(self):
        return self.__coffee_type

    def get_size(self):
        return self.__size

    def get_milk(self):
        return self.__milk

    def get_flavor(self):
        return self.__flavor

    def get_pump_level(self):
        return self.__pump_level

    def get_cost(self):
        return self.__cost

    # --- Setters ✍️ ---
    # Setters are less common when logic is handled by other methods,
    # but they are included here for completeness.
    def set_coffee_type(self, coffee_type):
        self.__coffee_type = coffee_type

    def set_size(self, size):
        self.__size = size

    def set_milk(self, milk):
        self.__milk = milk

    def set_flavor(self, flavor):
        self.__flavor = flavor

    def set_pump_level(self, pump_level):
        self.__pump_level = pump_level

    def set_cost(self, cost):
        self.__cost = cost

    # --- Magic Method: __str__ 💬 ---
    # This replaces the old `get_summary()` method.
    # It provides a user-friendly receipt of the order.
    def __str__(self):
        # The .strftime() method formats the timestamp into a readable string.
        formatted_time = self.__timestamp.strftime("%Y-%m-%d %I:%M %p")
        # The :.2f formats the cost to two decimal places (like money).
        emp_name = f"{self.__employee.get_fname()} {self.__employee.get_lname()}"
        return (
            f"☕ ---- RECEIPT ---- ☕\n"
            f"Order for: {emp_name}\n"
            f"Time: {formatted_time}\n"
            f"-----------------------\n"
            f"Item: {self.__size} {self.__coffee_type}\n"
            f" - Milk: {self.__milk}\n"
            f" - Flavor: {self.__flavor} ({self.__pump_level})\n"
            f"-----------------------\n"
            f"TOTAL: ${self.__cost:.2f}\n"
            f"-----------------------"
        )

    # --- Main Logic Methods ---

    def calculate_cost(self, menu: Menu):
        """
        🧮 FINAL LOGIC: Calculates the total cost of the coffee order.
        - Base price is from the SIZE.
        - Upcharge is from the PUMP LEVEL.
        """
        base_price = 0.0
        # Find the price for the selected size.
        # The menu.prices is a list like ['Small: 3.00', 'Medium: 4.00']
        for price_entry in menu.get_prices():
            size_name, price_str = price_entry.split(':')
            if size_name.strip().lower() == self.__size.lower():
                base_price = float(price_str.strip())
                break  # Found the price, no need to look further

        # Add cost for flavor based on the pump level.
        flavor_upcharge = 0.0
        if self.__flavor.lower() != "none":
            level = self.__pump_level.split(':')[0].strip().lower()
            if level == "light":
                flavor_upcharge = 0.25
            elif level == "normal":
                flavor_upcharge = 0.50
            elif level == "heavy":
                flavor_upcharge = 0.75

        # Set the final cost on the object
        self.__cost = base_price + flavor_upcharge

    def save(self):
        """💾 Saves the completed order to the orders.txt file."""
        # --- PATH CORRECTION ---
        # Build a robust path to 'orders.txt' inside the 'MontysOOP' folder.
        # os.path.dirname(__file__) gets the directory of this script.
        # os.path.join() creates a correct path for any OS.
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "orders.txt")

        # Format the order string to be saved in the file.
        order_string = (
            f"{self.__employee.get_emp_num()},{self.__timestamp.isoformat()},"
            f"{self.__coffee_type},{self.__size},{self.__milk},"
            f"{self.__flavor},{self.__pump_level},{self.__cost:.2f}\n"
        )
        try:
            # Use the full, correct path to open the file.
            with open(file_path, "a") as f:  # 'a' for append mode
                f.write(order_string)
            print("✅ Order saved successfully!")
        except IOError as e:
            print(f"🔥 Error saving order: {e}")

    # --- Factory Classmethod 🏭 ---
    @classmethod
    def from_input(cls, employee: Employee, menu: Menu):
        """
        CORRECTED LOGIC: Factory method to create a Coffee object.
        It asks for coffee, then size, then milk, etc., separately.
        """
        print("\n☕ Let's create a new coffee order!")

        # --- 1. Choose Coffee Type ---
        print("\n--- Coffee Options ---")
        # We use enumerate to get a number for each item (e.g., 1. Latte)
        coffee_options = menu.get_coffee()
        for i, item in enumerate(coffee_options):
            print(f"  {i+1}. {item}")
        while True:
            try:
                choice = int(input("Select a coffee type: "))
                if 1 <= choice <= len(coffee_options):
                    coffee_type = coffee_options[choice - 1]
                    break
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # --- 2. Choose Size ---
        print("\n--- Size Options ---")
        size_options = [s.split(':')[0].strip() for s in menu.get_prices()]
        for i, item in enumerate(size_options):
            print(f"  {i+1}. {item}")
        while True:
            try:
                choice = int(input("Select a size: "))
                if 1 <= choice <= len(size_options):
                    size = size_options[choice - 1]
                    break
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # --- 3. Choose Milk ---
        print("\n--- Milk Options ---")
        milk_options = menu.get_milks()
        for i, item in enumerate(milk_options):
            print(f"  {i+1}. {item}")
        while True:
            try:
                choice = int(input("Select a milk type: "))
                if 1 <= choice <= len(milk_options):
                    milk = milk_options[choice - 1]
                    break
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # --- 4. Choose Flavor ---
        print("\n--- Flavor Options ---")
        flavor_options = menu.get_flavors()
        for i, item in enumerate(flavor_options):
            print(f"  {i+1}. {item}")
        while True:
            try:
                choice = int(input("Select a flavor (or 'None'): "))
                if 1 <= choice <= len(flavor_options):
                    flavor = flavor_options[choice - 1]
                    break
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # --- 5. Choose Pump Level ---
        pump_level = "None"  # Default to None
        if flavor.lower() != "none":
            print(f"\n--- Pump Options for {flavor} ---")
            pump_options = menu.get_pumps()
            for i, item in enumerate(pump_options):
                print(f"  {i+1}. {item}")
            while True:
                try:
                    choice = int(input("Select a pump level: "))
                    if 1 <= choice <= len(pump_options):
                        pump_level = pump_options[choice - 1]
                        break
                    else:
                        print("Invalid number. Please choose from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Now we have all the info to create a temporary object.
        new_order = cls(employee, coffee_type, size, milk, flavor, pump_level)

        # Use the object's own method to calculate its cost based on the menu.
        new_order.calculate_cost(menu)

        # Return the fully formed, ready-to-go Coffee object.
        return new_order


# --- Test Area ---
if __name__ == "__main__":
    print("--- 🧪 Testing Coffee Class 🧪 ---")

    # We need a mock Employee and Menu to test.
    test_emp = Employee("Testy", "McTesterson", "1234", 999)

    # --- PATH CORRECTION for testing ---
    # Build a robust path to 'menu.txt' for the test run.
    script_dir = os.path.dirname(__file__)
    menu_file_path = os.path.join(script_dir, "menu.txt")

    try:
        # Use the full, correct path to load the menu.
        test_menu = Menu.from_file(menu_file_path)

        if test_menu:  # Proceed only if menu loaded successfully
            # 1. Test the from_input() factory method
            print("\n--- 1. Testing from_input() ---")
            # This will prompt you to enter an order in the terminal.
            my_order = Coffee.from_input(test_emp, test_menu)

            # 2. Test the __str__() method (the receipt)
            print("\n--- 2. Testing __str__() ---")
            print(my_order)

            # 3. Test the save() method
            print("\n--- 3. Testing save() ---")
            my_order.save()
            print("Check 'MontysOOP/orders.txt' to see if the order was saved.")
        else:
            print("\n🔥 ERROR: Could not load menu. Aborting tests.")

    except FileNotFoundError:
        print(
            f"\n🔥 ERROR: '{menu_file_path}' not found. "
            "Cannot run tests without the menu file."
        )
