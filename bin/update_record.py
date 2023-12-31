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
from library.parse_notion_input import parse_notion_input
from library.input_shcn import input_shcn

def update_record():
    # Locate the record in mungo to update
    print("Update Record:")
    qrcode = parse_qrcode_input()
    
    selected_record = get_record_by_identifier(qrcode)
    
    if selected_record:
        print_inventory(selected_record)
        mungo_id = selected_record['identifier']
        mungo_notion = selected_record.get('notion_id')

        # Create, review, or update the link the record to Notion.
        notion_id = parse_notion_input(mungo_notion)
        
        # Get the shelving location for the item, and parse out the specifics.
        shcn, shelf, bay, container, slot, analysis = input_shcn()

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
        if mungo_type is not None:
            update_fields["$set"]["type"] = mungo_type
        
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