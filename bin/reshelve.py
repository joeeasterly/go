"""
This script is used to reshelve items in an inventory system. It prompts the user to input an SHCN record, which includes information about the item's location in the inventory system. The script then scans a QR code to identify the item and updates the item's record in the inventory system with the new location information. The updated record is then printed to the console.

Functions:
- audit_items(shcn, shelf, bay, container, slot): Prompts the user to scan a QR code and updates the item's record in the inventory system with the new location information.
"""
from lib_git import generate_recset_by_id
from lib_identifier import parse_qrcode_input
from lib_mungo import get_record_by_identifier
from lib_shcn import parse_shcn_input
from update_record_by_identifier import update_record_by_identifier
from reshelve_notion_inventory import reshelve_notion_inventory
from print_inventory import print_inventory
from datetime import datetime

def reshelve_record():
    shcn, shelf, bay, container, slot, analysis = parse_shcn_input()
    while True:
        mungo_id = parse_qrcode_input()
        if mungo_id == "exit_loop":
            break
        # Get the notion_id
        record = get_record_by_identifier(mungo_id)
        notion_id = record.get("notion_id")
        # Construct the update_fields dictionary
        update_fields = {
            "$set": {
                "identifier": mungo_id,
                "shcn": shcn,
                "allocated": True,
                "class": "inventory",
                "last_updated": datetime.now()
            }
        }
        # Construct the unset_fields dictionary
        unset_fields = {
            "$unset": {
                "unsetted": ""
            }
        }

        if shelf is not None:
            update_fields["$set"]["shelf"] = shelf
        else:
            unset_fields["$unset"]["shelf"] = ""
        
        if bay is not None:
            update_fields["$set"]["bay"] = bay
        else:
            unset_fields["$unset"]["bay"] = ""
        
        if container is not None:
            update_fields["$set"]["container"] = container
        else:
            unset_fields["$unset"]["container"] = ""
        
        if slot is not None:
            update_fields["$set"]["slot"] = slot
        else:
            unset_fields["$unset"]["slot"] = ""

        # Update the record
        update_record_by_identifier(update_fields, unset_fields)
        generate_recset_by_id(mungo_id)
        # Update the Notion inventory
        reshelve_notion_inventory(notion_id, shcn)
        print_inventory(get_record_by_identifier(mungo_id))
        print ("scan additional item(s) or press * to quit")