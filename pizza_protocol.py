class Pizza:
    # Class attributes for the options
    base_options = ["Neapolitan Crust", "New York-Style Crust", "Chicago Deep Dish Crust"]
    cheese_options = ["Mozzarella", "Cheddar", "Parmesan"]
    sauce_options = ["Tomato Sauce", "Marinara Sauce", "Pesto"]
    topping_options = ["Pepperoni", "Bacon", "Chicken", "Mushrooms", "Onions", "Bell Peppers"]

    def __init__(self):
        self.base = ""
        self.cheese = ""
        self.sauce = ""
        self.toppings = []

    def set_base(self, base):
        self.base = base

    def set_cheese(self, cheese):
        self.cheese = cheese

    def set_sauce(self, sauce):
        self.sauce = sauce

    def add_topping(self, topping):
        self.toppings.append(topping)

    def remove_topping(self, topping):
        if topping in self.toppings:
            self.toppings.remove(topping)

    def get_pizza_details(self):
        return {
            "Base": self.base,
            "Cheese": self.cheese,
            "Sauce": self.sauce,
            "Toppings": self.toppings,
        }
    
    @classmethod
    def print_options(cls):
        print("Base Options:", cls.base_options)
        print("Cheese Options:", cls.cheese_options)
        print("Sauce Options:", cls.sauce_options)
        print("Topping Options:", cls.topping_options)

# Example usage:
my_pizza = Pizza()
my_pizza.set_base("Thin Crust")
my_pizza.set_cheese("Mozzarella")
my_pizza.set_sauce("Tomato")
my_pizza.add_topping("Pepperoni")
my_pizza.add_topping("Mushrooms")

print(my_pizza.get_pizza_details())

# Printing available options
Pizza.print_options()
