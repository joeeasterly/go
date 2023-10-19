from library.allocate_notion_id import allocate_notion_id
import time
def parse_notion_input(notion_id=None):
    notion_input = input(f"Enter Notion ID (INV-) [{notion_id}]: ")
    if notion_input == "" and notion_id is None:
        notion_id = allocate_notion_id()
        print(f"Allocating Notion Inventory ID {notion_id}")
    elif notion_input != "":
        notion_id = notion_input.to_lower()
        notion_id = notion_id.replace("inv-", "")
        if not notion_id.isdigit():
            raise ValueError("Notion ID must be a number (apart from prefix).")
        print(f"Using Notion Inventory ID {notion_id}")
        time.sleep(1) # Play nice with the Notion API
    return notion_id