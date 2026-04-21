from MontysOOP.Menu import Menu
from MontysOOP.Employee import Employee
from MontysOOP.Coffee import Coffee
import os


def print_label(order):
    print("\n--- Order Label ---")
    print(order)
    print("-------------------\n")


def main():
    print("Welcome to Monty's OOP Coffee Ordering System! ☕\n")

    # 1. Employee login/creation
    employee = Employee.from_input()

    # 2. Load the menu (always from the same folder as this script)
    script_dir = os.path.dirname(__file__)
    menu_file_path = os.path.join(script_dir, "menu.txt")
    menu = Menu.from_file(menu_file_path)
    if not menu:
        print("Menu could not be loaded. Exiting.")
        return

    orders = []  # In-memory list for this session
    while True:
        print("\n--- Main Menu ---")
        print("1. Place a new order")
        print("2. View my orders (this session)")
        print("3. Update an order")
        print("4. Delete an order")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            order = Coffee.from_input(employee, menu)
            print_label(order)
            confirm = input(
                "Is this order correct? (y = save, u = update, d = delete/cancel): ").lower()
            if confirm == "y":
                order.save()
                orders.append(order)
                print("Order saved!")
            elif confirm == "u":
                print("Let's update your order.")
                order = Coffee.from_input(employee, menu)
                print_label(order)
                confirm2 = input("Save this updated order? (y/n): ").lower()
                if confirm2 == "y":
                    order.save()
                    orders.append(order)
                    print("Order saved!")
                else:
                    print("Order not saved.")
            elif confirm == "d":
                print("Order cancelled.")
            else:
                print("Invalid input. Order not saved.")

        elif choice == "2":
            if not orders:
                print("No orders this session yet.")
            else:
                print("\n--- Your Orders This Session ---")
                for idx, o in enumerate(orders, 1):
                    print(f"Order #{idx}:")
                    print_label(o)

        elif choice == "3":
            if not orders:
                print("No orders to update.")
            else:
                for idx, o in enumerate(orders, 1):
                    print(
                        f"{idx}. {o.get_size()} {o.get_coffee_type()} ({o.get_flavor()}, {o.get_pump_level()})")
                sel = input("Enter order number to update: ")
                if sel.isdigit() and 1 <= int(sel) <= len(orders):
                    idx = int(sel) - 1
                    print("Updating order:")
                    orders[idx] = Coffee.from_input(employee, menu)
                    orders[idx].save()
                    print("Order updated and saved.")
                else:
                    print("Invalid selection.")

        elif choice == "4":
            if not orders:
                print("No orders to delete.")
            else:
                for idx, o in enumerate(orders, 1):
                    print(
                        f"{idx}. {o.get_size()} {o.get_coffee_type()} ({o.get_flavor()}, {o.get_pump_level()})")
                sel = input("Enter order number to delete: ")
                if sel.isdigit() and 1 <= int(sel) <= len(orders):
                    idx = int(sel) - 1
                    print("Deleting order:")
                    print_label(orders[idx])
                    confirm = input("Are you sure? (y/n): ").lower()
                    if confirm == "y":
                        del orders[idx]
                        print("Order deleted (from session, not file).")
                    else:
                        print("Delete cancelled.")
                else:
                    print("Invalid selection.")

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
