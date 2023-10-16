import pymongo
import requests
import json
import os
from pprint import pprint
from datetime import datetime
from allocate_notion_id import allocate_notion_id
from link_notion_inventory import link_notion_inventory
from get_notion_record import get_notion_record
from print_inventory import print_inventory

def add_storage():
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    print("Add SHCN Record Record:")
    input_shelf = input(f"Enter SHCN: ")
    shelf_length = len(input_shelf)
    identifier = allocated = shelf = bay = container = slot = None
    analysis = None
    if shelf_length == 1:
        raise ValueError("SHCN must between two and five hex digits.")
    if shelf_length >= 2:
        shelf = input_shelf[:2]
        analysis = "Shelf: " + shelf
    if shelf_length >= 3:
        bay = input_shelf[:3]
        analysis = analysis + ", Bay: " + bay
    if shelf_length >= 4:
        container = input_shelf[:4]
        analysis = analysis + ", Container: " + container
    if shelf_length >= 5:
        slot = input_shelf[:5]
        analysis = analysis + ", Slot: " + slot
    if shelf_length >= 6:
        if "https://joeeasterly.github.io/go/" in input_shelf:  # Checking in input_shelf, not identifier
            identifier = input_shelf.replace("https://joeeasterly.github.io/go/", "")
            if len(identifier) != 4:  # Ensuring the identifier has exactly 4 digits
                raise ValueError("Identifier following the URL must have exactly 4 digits.")
        else:
            raise ValueError("SHCN must between two and five hex digits.")

    print("Input analysis: " + analysis)

    if shelf_length == 4:
        identifier = input_shelf
        filter_criteria = {"identifier": identifier}
        existing_record = collection.find_one(filter_criteria)
        if existing_record:
            allocated = existing_record.get('allocated')
            if allocated:
                raise ValueError(f"Warning: identifier/shcn collision: " + identifier + ". Fix it first in mongodb compass and try again.")
    
    # Choose between a pre-printed QR Code, or allocate a new one
    filter_criteria = ""
    choose_code = input("Enter QR code or (blank to auto-assign): ")
    if choose_code == "":
        # Allocate an identifier for a new record in mongodb
        search_criteria = {"allocated": False}
        filter_criteria = [
            {"$match": search_criteria},
            {"$sample": {"size": 1}}
        ]
        new_record = list(collection.aggregate(filter_criteria))
        selected_record = new_record[0]
    else:
        filter_criteria = {"identifier": choose_code}
        new_record = collection.find_one(filter_criteria)
        selected_record = new_record

    if new_record:
        if choose_code == "":
            print(f"Allocating Identifier {selected_record['identifier'].upper()}")
        else:
            print(f"Using Identifier {selected_record['identifier'].upper()}")
        mungo_id = selected_record['identifier']
        notion_id = input("Enter Notion ID: ")
        label = input("Enter Label: ")

        if notion_id == "":
            notion_id = allocate_notion_id()
            print(f"Allocating Notion Inventory ID {notion_id}")

        if label == "":
            notion_record = get_notion_record(notion_id)
            label = notion_record.get('properties', {}).get('Name', {}).get('title', [])[0].get('plain_text', '')

        last_updated = datetime.now()
        
        update_fields = {
            "$set": {
                "notion_id": notion_id,
                "type": "storage",
                "class": "inventory",
                "label": label,
                "last_updated": last_updated,
                "allocated": True
            }
        }
        #  Conditionally add fields if they exist
        if shelf is not None:
            update_fields["$set"]["shelf"] = shelf
        if bay is not None:
            update_fields["$set"]["bay"] = bay
        if container is not None:
            update_fields["$set"]["container"] = container
        if slot is not None:
            update_fields["$set"]["slot"] = slot

        collection.update_one({"_id": selected_record["_id"]}, update_fields)
        link_notion_inventory(notion_id, mungo_id, label)
        print("Record updated successfully.")

        confirmation_query = {"_id": selected_record["_id"]}
        confirmation_record = collection.find_one(confirmation_query)
        print("Updated record:")
        pprint(confirmation_record)
    

# Run the update_record function if this script is run directly
if __name__ == "__main__":
    add_storage()