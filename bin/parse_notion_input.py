from bin.allocate_notion_id import allocate_notion_id
import time

def parse_notion_input(mungo_notion=""):
    # Prompt the user for input
    if mungo_notion:
        user_input = input(f"Notion ID: [{mungo_notion}] Enter to keep existing ID: ").lower().strip()
    else:
        user_input = input(f"Notion ID: [{mungo_notion}] Enter to allocate new ID: ").lower().strip()

    # If user inputs "+" or "new", allocate a new Notion ID
    if user_input in ["+", "new"]:
        notion_id = allocate_notion_id()
        print(f"Allocating Notion Inventory ID {notion_id}")

    # If user hits return/enter without any input, use the default behavior
    elif not user_input:
        if mungo_notion:
            notion_id = mungo_notion  # Use the existing mungo_notion if it exists
            print(f"Using existing Notion Inventory ID {notion_id}")
        else:
            notion_id = allocate_notion_id()  # Allocate a new notion_id if mungo_notion doesn't exist
            print(f"Allocating Notion Inventory ID {notion_id}")

    # Validate and use the user's input if provided and not a special keyword
    else:
        user_input = user_input.replace("inv-", "")  # Remove the prefix if present
        if not user_input.isdigit():
            raise ValueError("Notion ID must be a number (apart from prefix).")
        notion_id = user_input
        print(f"Using Notion Inventory ID {notion_id}")

    time.sleep(1)  # Play nice with the Notion API
    return notion_id