import pymongo
from datetime import datetime
import time
from library.link_notion_inventory import link_notion_inventory
from library.print_inventory import print_inventory
from library.parse_qrcode_input import parse_qrcode_input
from library.get_record_by_identifier import get_record_by_identifier
from library.update_record_by_identifier import update_record_by_identifier
from library.allocate_notion_id import allocate_notion_id
from library.get_notion_record import get_notion_record
from library.input_shcn import input_shcn

def update_record():
    print("Update Record:")
    
    qrcode = parse_qrcode_input()
    
    selected_record = get_record_by_identifier(qrcode)
    
    if selected_record:
        print_inventory(selected_record)
        mungo_id = selected_record['identifier']
        notion_id = input(f"Enter Notion ID (INV-) [{selected_record.get('notion_id')}]: ")
        if notion_id == "":
            notion_id = allocate_notion_id()
            print(f"Allocating Notion Inventory ID {notion_id}")
            time.sleep(1) # Play nice with the Notion API

        # notion_record = get_notion_record(notion_id)
        # notion_label = notion_record.get('properties', {}).get('Name', {}).get('title', [])[0].get('plain_text', '')
        shcn, shelf, bay, container, slot, analysis = input_shcn()
        mungo_label = selected_record.get('label')
        if mungo_label is None:
            input_label_display = ""
        else:
            input_label_display = "[" + mungo_label + "]"
        
        input_label = input(f"Enter Label: " + input_label_display)
        if input_label != "":
            label = input_label
        else:
            label = mungo_label

        # Construct the update_fields dictionary
        update_fields = {
            "$set": {
                "identifier": mungo_id,
                "label": label,
                "allocated": True,
                "class": "inventory",
                "last_updated": datetime.now()
            }
        }
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
        if notion_id is not None:
            update_fields["$set"]["notion_id"] = notion_id
        
        # Update the record
        update_record_by_identifier(update_fields)

        # Sync the record to Notion.
        link_notion_inventory(notion_id, mungo_id, shcn, label)
        print("Record updated successfully.")
        print_inventory(get_record_by_identifier(qrcode))
    else:
        raise Exception(f"Record {qrcode} not found.")

# Run the update_record function if this script is run directly
if __name__ == "__main__":
    update_record()