import pymongo
from datetime import datetime
from library.archive_notion_page import archive_notion_page
from library.print_inventory import print_inventory
from library.connect_mungo import connect_mungo
from library.parse_qrcode_input import parse_qrcode_input
def delete_consumable():
    print("~Delete Consumable~")
    identifier = parse_qrcode_input()
    collection = connect_mungo()
    filter_criteria = {"identifier": identifier}
    existing_record = collection.find_one(filter_criteria)
    if existing_record:
        print_inventory(existing_record)
        update_fields = {
            "$set": {
                "allocated": False,
                "target": "#",
                "last_updated": datetime.now()
                }
            }
        unset_fields = {
            "$unset": {
                "class": "",
                "permalink": "",
                "staged": "",
                "bay": "",
                "expires": "",
                "label": "",
                "notion_id": "",
                "percentage": "",
                "quantity": "",
                "shcn": "",
                "shelf": "",
                "type": "",
                "upc": ""
                }
        }
        delete_confirmation = input("Delete this record? [y/N]: ")
        if delete_confirmation.lower() == "y":
            archive_notion_page(existing_record.get("notion_id"))
            # Merge update_fields and unset_fields into a single update operation
            update_operation = {**update_fields, **unset_fields}

            # Apply the update
            collection.update_one({"identifier": identifier}, update_operation)
            print("Record deleted.")
        else:
            print("Record not deleted.")
    else:
        print("No record found.")