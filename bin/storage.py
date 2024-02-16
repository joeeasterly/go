import pymongo
from datetime import datetime
from lib_mungo import connect_mungo, get_record_by_identifier, allocate_identifier
from lib_shcn import parse_shcn_input
from lib_notion import allocate_notion_id, link_notion_inventory, parse_notion_input
from lib_identifier import parse_qrcode_input
from print_inventory import print_inventory


def add_storage():
    print("Add SHCN Record:")
    shcn, shelf, bay, container, slot, analysis = parse_shcn_input()
    print(analysis)

    mungo_id = parse_qrcode_input()
    
    if mungo_id == "":
        selected_record = allocate_identifier()
    else:
        selected_record = get_record_by_identifier(mungo_id)

    if selected_record:
        if mungo_id == "":
            print(f"Allocating Identifier {selected_record['identifier'].upper()}")
        else:
            print(f"Using Identifier {selected_record['identifier'].upper()}")
        mungo_id = selected_record['identifier']
        notion_id = parse_notion_input()

        if notion_id == "":
            notion_id = allocate_notion_id()
            print(f"Allocating Notion Inventory ID {notion_id}")
       
        update_fields = {
            "$set": {
                "notion_id": notion_id,
                "type": "storage",
                "class": "inventory",
                "last_updated": datetime.now(),
                "allocated": True
            }
        }
        #  Conditionally add fields if they exist
        if shcn is not None:
            update_fields["$set"]["shcn"] = shcn
            default_label = f"SHCN {shcn}"
        if shelf is not None:
            update_fields["$set"]["shelf"] = shelf
            default_label = f"shelf {shelf}"
        if bay is not None:
            update_fields["$set"]["bay"] = bay
            default_label = f"bay {bay}"
        if container is not None:
            update_fields["$set"]["container"] = container
            default_label = f"container {container}"
        if slot is not None:
            update_fields["$set"]["slot"] = slot
            default_label = f"slot {slot}"
        
        label = default_label
        label_input = input(f"Enter Label: ({default_label}) ")
        if label_input != "":
            label = label_input
        update_fields["$set"]["label"] = label

        collection = connect_mungo()
        collection.update_one({"_id": selected_record["_id"]}, update_fields)
        link_notion_inventory(notion_id, mungo_id, shcn, label)
        print("Mungo Record updated successfully.")

        confirmation_query = {"_id": selected_record["_id"]}
        confirmation_record = collection.find_one(confirmation_query)
        print_inventory(confirmation_record)

# Do add_storage() if this script is run directly
if __name__ == "__main__":
    add_storage()