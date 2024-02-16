"""This module parses the percentage remaining of a 
consumable item from the user."""
def parse_percentage():
    percentage = input("Percentage of item remaining: ")
    # If the user enters a percentage with a percent sign, remove it.
    if percentage.endswith("%"):
        percentage = float(percentage.replace("%", ""))
    # If the user enters a percentage with a decimal, multiply it by 100.
    if "." in percentage:
        percentage = float(percentage) * 100
    # If the user enters a letter, return an error message.
    if not percentage:
        print("Please enter a number.")
        return parse_percentage()
    return percentage

def parse_quantity(existing_quantity = None):
    # Prompt the user to enter the number of copies of an item.
    quantity_prompt = "Enter item count: "
    if existing_quantity:
        quantity_prompt = f"Enter item count [{existing_quantity}]: "
    quantity = input(quantity_prompt)
    # If the user does not enter a number, use the existing quantity instead.
    if not quantity:
        quantity = existing_quantity
    # If the user enters a letter, return an error message.
    if not quantity.isnumeric():
        print("Please enter a number.")
        return parse_quantity()
    return quantity


