import pymongo
from datetime import datetime
import time
from link_notion_inventory import link_notion_inventory
from print_inventory import print_inventory
from parse_qrcode_input import parse_qrcode_input
from get_record_by_identifier import get_record_by_identifier
from update_record_by_identifier import update_record_by_identifier
from get_last_record import get_last_record
from allocate_notion_id import allocate_notion_id
from get_notion_record import get_notion_record
from parse_notion_input import parse_notion_input
from parse_shcn_input import parse_shcn_input

def update_record():
    # Locate the record in mungo to update
    print("Update Record:")
    qrcode = parse_qrcode_input()
    
    selected_record = get_record_by_identifier(qrcode)
    last_record = get_last_record()
    
    if selected_record:
        print_inventory(selected_record)
        mungo_id = selected_record['identifier']
        mungo_notion = selected_record.get('notion_id')

        # Create, review, or update the link the record to Notion.
        notion_id = parse_notion_input(mungo_notion)
        notion_title = None
        if notion_id is not None:
            notion_record = get_notion_record(notion_id)
            notion_title = notion_record.get('properties').get('Name').get('title')[0].get('text').get('content')
        
        # Get the shelving location for the item, and parse out the specifics.
        shcn, shelf, bay, container, slot, analysis = parse_shcn_input()

        # If type is not storage, set it to item.
        mungo_type = selected_record.get('type')
        if mungo_type is None:
            mungo_type = "item"
        elif mungo_type == "storage":
            mungo_type = "storage"
        else:
            mungo_type = "item"

        # Create, review, or update the label for the item.
        mungo_label = selected_record.get('label')
        if mungo_label is None and notion_title is None:
            input_label_display = ""
            default_label = ""
        elif mungo_label is None and notion_title is not None:
            input_label_display = "[" + notion_title + "]"
            default_label = notion_title
        else:
            input_label_display = "[" + mungo_label + "]"
            default_label = mungo_label
        
        input_label = input(f"Enter Label: " + input_label_display)
        if input_label != "":
            if input_label == "+":
                label = last_record.get('label')
            else:
                label = input_label
        else:
            label = default_label

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
        unset_fields = {
            "$unset": {
                "unsetted": ""
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
        if mungo_type is not None:
            update_fields["$set"]["type"] = mungo_type
        
        if not shelf:
            unset_fields["$unset"]["shelf"] = ""
        if not bay:
            unset_fields["$unset"]["bay"] = ""
        if not container:
            unset_fields["$unset"]["container"] = ""
        if not slot:
            unset_fields["$unset"]["slot"] = ""
        
        # Update the record
        update_record_by_identifier(update_fields, unset_fields)

        # Sync the record to Notion.
        link_notion_inventory(notion_id, mungo_id, shcn, label)
        print("Record updated successfully.")
        print_inventory(get_record_by_identifier(qrcode))
    else:
        raise Exception(f"Record {qrcode} not found.")

# Run the update_record function if this script is run directly
if __name__ == "__main__":
    update_record()