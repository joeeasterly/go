import pymongo
from pprint import pprint
from datetime import datetime
from library.link_notion_consumable import link_notion_consumable  # Import the function
from library.print_inventory import print_inventory
from library.connect_mungo import connect_mungo
from library.parse_date import parse_date
from library.parse_qrcode_input import parse_qrcode_input
from library.parse_percentage import parse_percentage
from library.parse_quantity import parse_quantity
from library.parse_label import parse_label
from library.parse_upc import parse_upc
from library.parse_notion_input import parse_notion_input
from library.input_shcn import input_shcn

def update_consumable():
    
    print("Update Consumable:")
    identifier = parse_qrcode_input()
    
    collection = connect_mungo()
    
    filter_criteria = {"identifier": identifier}
    existing_record = collection.find_one(filter_criteria)
    if existing_record:
        print("Current Record:")
        pprint(existing_record)
        upc, upc_label = parse_upc(existing_upc=existing_record.get("upc"))
        existing_label = existing_record.get("label")
        if existing_label:
            default_label = existing_label
        elif upc_label:
            default_label = upc_label
        else:
            default_label = None
        label = parse_label(default_label)
        expires = parse_date(message = "Expiration Date: ")
        percentage = parse_percentage()
        shcn, shelf, bay, container, slot, analysis = input_shcn(existing_shcn=existing_record.get("shcn"))
        quantity = parse_quantity(existing_quantity=existing_record.get("quantity"))

        # Create, review, or update the link the record to Notion.
        notion_id = parse_notion_input(mungo_notion = existing_record.get("notion_id"))

        update_fields = {
            "$set": {
                "type": "consumable",
                "last_updated": datetime.now()
            }
        }
        #  Conditionally add fields if they exist
        if notion_id is not None:
            update_fields["$set"]["notion_id"] = notion_id
        if upc is not None:
            update_fields["$set"]["upc"] = upc
        if label is not None:
            update_fields["$set"]["label"] = label
        if expires is not None:
            update_fields["$set"]["expires"] = expires
        if percentage is not None:
            update_fields["$set"]["percentage"] = percentage
        if quantity is not None:
            update_fields["$set"]["quantity"] = quantity
        if shcn is not None:
            update_fields["$set"]["shcn"] = shcn
        if shelf is not None:
            update_fields["$set"]["shelf"] = shelf
        if bay is not None:
            update_fields["$set"]["bay"] = bay
        if container is not None:
            update_fields["$set"]["container"] = container
        if slot is not None:
            update_fields["$set"]["slot"] = slot

        result = collection.update_one(filter_criteria, update_fields)
        
        if result.matched_count > 0:
            updated_record = collection.find_one(filter_criteria)
            print("Record updated successfully!")
            print()
            print_inventory(updated_record)
            # If notion_id is provided, call the update_notion_record function
            if notion_id:
                update_result = link_notion_consumable(notion_id, identifier, shcn, label, expires, upc, percentage, quantity)
                print(update_result)
        else:
            print("No record found with the provided identifier.")
    else:
        print("No record found with the provided identifier.")

# You can also include error handling and validation as needed. 