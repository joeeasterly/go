import pymongo
from pprint import pprint
from datetime import datetime
from library.input_shcn import input_shcn
from library.prevent_collision import prevent_collision
from library.parse_qrcode_input import parse_qrcode_input
from library.allocate_identifier import allocate_identifier
from library.get_record_by_identifier import get_record_by_identifier
from library.print_inventory import print_inventory
from library.allocate_notion_id import allocate_notion_id
from library.link_notion_inventory import link_notion_inventory
from library.get_notion_record import get_notion_record


def add_storage():
    print("Add SHCN Record:")
    shcn, shelf, bay, container, slot, analysis = input_shcn()
    print(analysis)

    prevent_collision(shcn)
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
        notion_id = input("Enter Notion ID: ")
        mungo_label = selected_record.get('label')
        

        if notion_id == "":
            notion_id = allocate_notion_id()
            print(f"Allocating Notion Inventory ID {notion_id}")

        notion_record = get_notion_record(notion_id)
       
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
        
        notion_label = notion_record.get('properties', {}).get('Name', {}).get('title', [])[0].get('plain_text', '')
        if notion_label is "allocated_by_mungo":
            label = default_label
        label_input = input(f"Enter Label: ({default_label}) ")
        if label_input != "":
            label = label_input
            update_fields["$set"]["label"] = label

        client = pymongo.MongoClient("mungo.local:27017")
        db = client["go"]
        collection = db["link"]
        collection.update_one({"_id": selected_record["_id"]}, update_fields)
        link_notion_inventory(notion_id, mungo_id, shcn, label)
        print("Mungo Record updated successfully.")

        confirmation_query = {"_id": selected_record["_id"]}
        confirmation_record = collection.find_one(confirmation_query)
        print_inventory(confirmation_record)

# Run the update_record function if this script is run directly
if __name__ == "__main__":
    add_storage()