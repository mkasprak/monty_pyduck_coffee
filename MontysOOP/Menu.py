
"""
    Menu Class
    Reads menu.txt and stores each section as a list of strings.
    This is an example of a class that handles file reading
    and organizes data into easy-to-use attributes.
"""
import os


class Menu:
    """
    A Menu object holds all the menu sections for Monty's Coffee.
    Each section is stored as a list of strings.

    Example usage:
        menu = Menu.from_file("menu.txt")
        print(menu.coffee)   # ['Espresso', 'Americano', ...]
        print(menu.prices)   # ['Small: 3.00', 'Medium: 4.00', ...]
    """

    def __init__(self, coffee, prices, milks, flavors, pumps):
        """
        The constructor sets up all the menu sections as attributes.
        Each attribute is a list of strings.
        'self' refers to this specific Menu object.
        """
        self.coffee = coffee    # List of coffee drink types
        self.prices = prices    # List of sizes and prices e.g. 'Small: 3.00'
        self.milks = milks      # List of milk options
        self.flavors = flavors  # List of flavor add-ins
        self.pumps = pumps      # List of pump options e.g. 'Light: 3'

    # --- Getter methods for OOP encapsulation ---
    def get_coffee(self):
        return self.coffee

    def get_prices(self):
        return self.prices

    def get_milks(self):
        return self.milks

    def get_flavors(self):
        return self.flavors

    def get_pumps(self):
        return self.pumps

    @classmethod
    def from_file(cls, filename="menu.txt"):
        """
        A classmethod that reads menu.txt and creates a Menu object.
        Each line in the file looks like:
            COFFEE ; Espresso, Americano, Latte, ...
        We split on ';' to get the header and the items,
        then split the items on ',' to get a list of strings.

        Usage:
            menu = Menu.from_file("menu.txt")
        """
        # Start with empty lists for each section
        menus = {}

        try:
            with open(filename, 'r') as file:
                for line in file:
                    # Skip blank lines
                    if ';' not in line:
                        continue

                    # Split each line into header and items
                    parts = line.strip().split(';')
                    header = parts[0].strip().upper()
                    # Split items by comma and strip extra spaces
                    items = [item.strip() for item in parts[1].split(',')]
                    menus[header] = items

            # Build and return the Menu object
            return cls(
                coffee=menus.get("COFFEE", []),
                prices=menus.get("PRICES", []),
                milks=menus.get("MILK", []),
                flavors=menus.get("FLAVORS", []),
                pumps=menus.get("PUMPS", [])
            )

        except FileNotFoundError:
            print(f"Error: '{filename}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred reading the menu: {e}")
            return None

    def __str__(self):
        """
        Defines what prints when you do print(menu).
        Lists each section and its options.
        """
        return (
            f"Coffee:  {self.coffee}\n"
            f"Prices:  {self.prices}\n"
            f"Milks:   {self.milks}\n"
            f"Flavors: {self.flavors}\n"
            f"Pumps:   {self.pumps}"
        )


# Quick test - only runs if you run Menu.py directly
if __name__ == "__main__":
    # Use a robust path to menu.txt in the same folder as this script
    script_dir = os.path.dirname(__file__)
    menu_file_path = os.path.join(script_dir, "menu.txt")
    menu = Menu.from_file(menu_file_path)
    if menu:
        print(menu)
