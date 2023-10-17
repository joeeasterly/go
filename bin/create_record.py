from datetime import datetime
from library.link_notion_inventory import link_notion_inventory
from library.get_notion_record import get_notion_record
from library.allocate_notion_id import allocate_notion_id
import pymongo
import random
from pprint import pprint

def random_prefix():
    initials = '123456789abcdefghijklmnopqrstuvwxyz'
    prefix = random.choice(initials) + random.choice(initials)
    return prefix

def create_record():
    print("Create Record:")
    
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]

    search_criteria = {"allocated": False}

    pipeline = [
        {"$match": search_criteria},
        {"$sample": {"size": 1}}
    ]

    matching_record = list(collection.aggregate(pipeline))

    if matching_record:
        selected_record = matching_record[0]
        print(f"Allocating Identifier {selected_record['identifier'].upper()}")

        mungo_id = selected_record['identifier']
        notion_id = input("Enter Notion ID: ")
        shelf = input("Enter Shelf: ")
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
                "shelf": shelf,
                "label": label,
                "last_updated": last_updated,
                "allocated": True
            }
        }
        collection.update_one({"_id": selected_record["_id"]}, update_fields)
        link_notion_inventory(notion_id, mungo_id, label)
        print("Record updated successfully.")

        confirmation_query = {"_id": selected_record["_id"]}
        confirmation_record = collection.find_one(confirmation_query)
        print("Updated record:")
        pprint(confirmation_record)