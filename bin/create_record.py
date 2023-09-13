from datetime import datetime
from get_notion_record import get_notion_record  # Renamed from link_notion_inventory
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

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        prefix = random_prefix()
        print(f"Attempting with prefix: {prefix}")

        search_criteria = {"identifier": {"$regex": f"^{prefix}"}, "allocated": False}
        matching_record = collection.find_one(search_criteria)

        if matching_record:
            print(f"Matching record found: {matching_record['identifier']}")

            notion_id = input("Enter Notion ID: ")
            shelf = input("Enter Shelf: ")
            label = input("Enter Label: ")

            if label == "":
                # Fetch the record from Notion using the notion_id
                notion_record = get_notion_record(notion_id)
                label = notion_record.get('Name', '')  # Replace '' with a default label if you wish

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
            
            collection.update_one({"_id": matching_record["_id"]}, update_fields)
            print("Record updated successfully.")

            confirmation_query = {"_id": matching_record["_id"]}
            confirmation_record = collection.find_one(confirmation_query)
            print("Updated record:")
            pprint(confirmation_record)
            break

        else:
            print("No matching record found, trying again...")
            attempts += 1

    if attempts == max_attempts:
        print(f"After {max_attempts} attempts, no unallocated identifier found.")