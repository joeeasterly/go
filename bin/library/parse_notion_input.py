from library.allocate_notion_id import allocate_notion_id
import time

def parse_notion_input(mungo_notion=""):
    notion_id = None
    notion_input = str(input(f"Enter Notion ID (INV-) [{mungo_notion}]: ")).lower().replace("inv-", "")

    # Validate and use the user's input if provided
    if notion_input:
        if not notion_input.isdigit():
            raise ValueError("Notion ID must be a number (apart from prefix).")
        notion_id = notion_input  # Update notion_id with user's input

    # Generate a new notion_id if none exists and the user didn't provide one
    elif not notion_id:
        notion_id = allocate_notion_id()
        print(f"Allocating Notion Inventory ID {notion_id}")
        print(f"Using Notion Inventory ID {notion_id}")
        time.sleep(1)  # Play nice with the Notion API

    return notion_id