from datetime import datetime
from pprint import pprint
import pymongo
from lib_git import generate_recset_by_id
from lib_notion import allocate_notion_id, link_notion_inventory, get_notion_record, parse_notion_input
from lib_mungo import allocate_identifier, get_record_by_identifier
from lib_shcn import parse_shcn_input
from lib_identifier import parse_qrcode_input
from update_record_by_identifier import update_record_by_identifier
from print_inventory import print_inventory

def create_record():
    print("Create Record:")
    mungo_id = parse_qrcode_input("Enter Mungo ID or leave blank: ")
    if mungo_id == "exit_loop":
        return
    if mungo_id == "":
        selected_record = allocate_identifier()
    else:
        selected_record = get_record_by_identifier(mungo_id)

    if selected_record:
        
        print(f"Allocating Identifier {selected_record['identifier'].upper()}")

        mungo_id = selected_record['identifier']
        notion_id = parse_notion_input()
        shcn = parse_shcn_input()
        mungo_label = input("Enter Label: ")

        if mungo_label == "":
            notion_record = get_notion_record(notion_id)
            mungo_label = notion_record.get('properties', {}).get('Name', {}).get('title', [])[0].get('plain_text', '')
        
        update_fields = {
            "$set": {
                "notion_id": notion_id,
                "identifier": mungo_id,
                "shcn": shcn,
                "class": "inventory",
                "type": "item",
                "label": mungo_label,
                "last_updated": datetime.now(),
                "allocated": True
            }
        }
        update_record_by_identifier(update_fields)
        link_notion_inventory(notion_id, mungo_id, shcn, mungo_label)
        generate_recset_by_id(mungo_id)
        print_inventory(get_record_by_identifier(mungo_id))
        print("Record updated successfully.")