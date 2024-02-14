import pymongo
from pprint import pprint
from datetime import datetime
from link_notion_consumable import link_notion_consumable  # Import the function
from print_inventory import print_inventory
from connect_mungo import connect_mungo
from parse_date_input import parse_date_input
from parse_qrcode_input import parse_qrcode_input
from parse_percentage import parse_percentage
from parse_quantity import parse_quantity
from parse_label import parse_label
from parse_upc import parse_upc
from parse_notion_input import parse_notion_input
from parse_shcn_input import parse_shcn_input
def add_consumable_instance():
    print("~Add Consumable Instance~")
    print("Enter source record:")
    source_identifier = parse_qrcode_input()
    print("Enter destination record:")
    destination_identifier = parse_qrcode_input()

    collection = connect_mungo()
    source_filter_criteria = {"identifier": source_identifier}
    destination_filter_criteria = {"identifier": destination_identifier}
    source_record = collection.find_one(source_filter_criteria)
    destination_record = collection.find_one(destination_filter_criteria)
    if source_record and destination_record:
        notion_id = source_record.get("notion_id")
        upc = source_record.get("upc")
        label = source_record.get("label")
        expires = source_record.get("expires")
        percentage = 100
        shcn = source_record.get("shcn")
        shelf = source_record.get("shelf")
        bay = source_record.get("bay")
        container = source_record.get("container")
        slot = source_record.get("slot")
        destination_quantity = 1
        source_quantity = float(source_record.get("quantity"))
        print(f"source quantity: {source_quantity}")
        mungo_type = "consumable_instance"
        destination_instance_of = source_identifier

        destination_update_fields = {
            "$set": {
                "type": "consumable",
                "last_updated": datetime.now(),
                "allocated": True
            }
        }
        #  Conditionally add fields if they exist
        if notion_id is not None:
            destination_update_fields["$set"]["notion_id"] = notion_id
        if upc is not None:
            destination_update_fields["$set"]["upc"] = upc
        if label is not None:
            destination_update_fields["$set"]["label"] = label
        if expires is not None:
            destination_update_fields["$set"]["expires"] = expires
        if percentage is not None:
            destination_update_fields["$set"]["percentage"] = percentage
        if shcn is not None:
            destination_update_fields["$set"]["shcn"] = shcn
        if shelf is not None:
            destination_update_fields["$set"]["shelf"] = shelf
        if bay is not None:
            destination_update_fields["$set"]["bay"] = bay
        if container is not None:
            destination_update_fields["$set"]["container"] = container
        if slot is not None:
            destination_update_fields["$set"]["slot"] = slot
        if destination_quantity is not None:
            destination_update_fields["$set"]["quantity"] = destination_quantity
        if mungo_type is not None:
            destination_update_fields["$set"]["type"] = mungo_type
        if destination_instance_of is not None:
            destination_update_fields["$set"]["instance_of"] = destination_instance_of

        source_update_fields = {
            "$set": {
                "type": "consumable",
                "last_updated": datetime.now()
            }
        }
        update_quantity = source_quantity + 1
        source_update_fields["$set"]["quantity"] = update_quantity

        # Update the record
        source_result = collection.update_one(source_filter_criteria, source_update_fields)
        destination_result = collection.update_one(destination_filter_criteria, destination_update_fields)
        if destination_result.matched_count > 0:
            destination_updated_record = collection.find_one(destination_filter_criteria)
            print("Instance added successfully!")
            print()
            print_inventory(destination_updated_record)
            # If notion_id is provided, call the update_notion_record function
            if notion_id:
                update_result = link_notion_consumable(notion_id, source_identifier, shcn, label, expires, upc, percentage, update_quantity)
                print(update_result)
    else:
        print("No record found with the provided identifier.")
