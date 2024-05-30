import pymongo
from datetime import datetime
from lib_git import generate_recset_by_id
from lib_notion import archive_notion_page
from print_inventory import print_inventory
from lib_mungo import connect_mungo
from lib_identifier import parse_qrcode_input
def delete_record():
    print("~Delete Record~")
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
            generate_recset_by_id(identifier)
            print("Record deleted.")
            print("Be sure to discard the inventory tag.")
        else:
            print("Record not deleted.")
    else:
        print("No record found.")