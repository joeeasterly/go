"""This module parses the number of copies/instances of an item from the user."""
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
