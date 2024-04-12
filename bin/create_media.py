from datetime import datetime
from pprint import pprint
import pymongo
from lib_message import red, yellow, green
from lib_notion import link_notion_media, get_notion_record, parse_notion_input
from lib_mungo import allocate_identifier, get_record_by_identifier
from lib_identifier import parse_qrcode_input
from update_record_by_identifier import update_record_by_identifier
from print_inventory import print_inventory

def create_media():
    print("Create Media Record:")
    mungo_id = parse_qrcode_input("Enter Mungo ID or leave blank: ")
    if mungo_id == "exit_loop":
        return
    if mungo_id == "":
        selected_record = allocate_identifier()
    else:
        selected_record = get_record_by_identifier(mungo_id)

    if selected_record:
        
        print(f"Allocating Identifier {yellow(selected_record['identifier'])}")

        mungo_id = selected_record['identifier']
        notion_id = parse_notion_input()
        mungo_label = input("Enter Label: ")

        if mungo_label == "":
            notion_record = get_notion_record(notion_id)
            mungo_label = notion_record.get('properties', {}).get('Name', {}).get('title', [])[0].get('plain_text', '')
        
        update_fields = {
            "$set": {
                "notion_id": notion_id,
                "identifier": mungo_id,
                "class": "media",
                "type": "work",
                "label": mungo_label,
                "last_updated": datetime.now(),
                "allocated": True
            }
        }
        update_record_by_identifier(update_fields)
        link_notion_media(notion_id, mungo_id, mungo_label)
        print_inventory(get_record_by_identifier(mungo_id))
        print("Record updated successfully.")