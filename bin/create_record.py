from datetime import datetime
from library.link_notion_inventory import link_notion_inventory
from library.get_notion_record import get_notion_record
from library.allocate_notion_id import allocate_notion_id
from library.parse_notion_input import parse_notion_input
from library.allocate_identifier import allocate_identifier
from library.update_record_by_identifier import update_record_by_identifier
from library.get_record_by_identifier import get_record_by_identifier
from library.input_shcn import input_shcn
from library.print_inventory import print_inventory
import pymongo
from pprint import pprint

def create_record():
    print("Create Record:")
    selected_record = allocate_identifier()

    if selected_record:
        
        print(f"Allocating Identifier {selected_record['identifier'].upper()}")

        mungo_id = selected_record['identifier']
        notion_id = parse_notion_input()
        shcn = input_shcn()
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
        print_inventory(get_record_by_identifier(mungo_id))
        print("Record updated successfully.")