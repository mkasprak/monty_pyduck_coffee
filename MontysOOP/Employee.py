""" 
    Demonstrate classes and objects based on the Monty coffee project
"""


class Employee:
    # class names are capitalized
    def __init__(self, fname, lname, extension, emp_num):
        # 🔐 These are the attributes of our class.
        # The double underscore `__` makes them "private".
        # This means they are intended to be accessed only from within this class.
        self.__fname = fname
        self.__lname = lname
        self.__extension = extension
        self.__emp_num = emp_num

    #  setters ✍️
    # A "setter" method is used to change the value of a private attribute.
    def set_fname(self, fname):
        self.__fname = fname

    def set_lname(self, lname):
        self.__lname = lname

    def set_extension(self, extension):
        self.__extension = extension

    def set_emp_num(self, emp_num):
        self.__emp_num = emp_num

    # getters 📥
    # A "getter" method is used to retrieve the value of a private attribute.
    def get_fname(self):
        return self.__fname

    def get_lname(self):
        return self.__lname

    def get_extension(self):
        return self.__extension

    def get_emp_num(self):
        return self.__emp_num

    # 💬 __str__ method
    # This is a special "magic method" in Python.
    # It returns a user-friendly string representation of the object.
    # Instead of creating a custom `description()` method, using __str__
    # lets us just `print(my_employee_object)` to see its details.
    def __str__(self):
        return (
            f"Employee: {self.__fname} {self.__lname}\n"
            f"  EMP#: {self.__emp_num}\n"
            f"  EXT: {self.__extension}"
        )

    # 🏭 @classmethod
    # This is a special kind of method that is bound to the class, not the instance.
    # We can call it on the class itself: `Employee.from_input()`
    # It's often used as a "factory" to create instances in different ways.
    # Here, we're using it to create an Employee object from user input.
    @classmethod
    def from_input(cls):
        """Factory method to create an Employee object from user input."""
        print("👤 Let's get your employee information.")
        fname = input("Enter your first name: ")
        lname = input("Enter your last name: ")
        # A simple loop to make sure we get a valid number for the extension.
        while True:
            try:
                extension = int(input("Enter your 4-digit phone extension: "))
                break  # Exit the loop if input is a valid integer
            except ValueError:
                print("Oops! That wasn't a valid number. Please try again.")
        while True:
            try:
                emp_num = int(input("Enter your employee number: "))
                break
            except ValueError:
                print("Oops! That wasn't a valid number. Please try again.")

        # `cls` here refers to the class itself (Employee).
        # So, `cls(fname, lname, extension, emp_num)` is the same as
        # `Employee(fname, lname, extension, emp_num)`.
        return cls(fname, lname, extension, emp_num)


# --- Test Area ---
# It's a good practice to have a small test block like this.
# The `if __name__ == "__main__":` part means this code will only run
# when you execute this file directly (e.g., `python Employee.py`),
# not when it's imported into another file.
if __name__ == "__main__":
    # Create an employee the "classic" way by passing arguments
    emp1 = Employee("Meri", "Kasprak", "8939", 222)
    print("--- Testing direct instantiation ---")
    print(emp1)  # This will automatically call the __str__ method!

    # Now, let's test our new factory method!
    print("\n--- Testing the from_input() factory method ---")
    emp_from_input = Employee.from_input()
    print("\nGreat, here is the employee object we created:")
    print(emp_from_input)  # This also calls __str__
