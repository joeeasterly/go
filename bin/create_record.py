# create_record.py
import pymongo
from pprint import pprint
from datetime import datetime
import random

def random_prefix():
    initials = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','j','k','m','n','p','q','r','s','t','u','v','w','x','y','z']
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

        # Search the MongoDB collection for an identifier where the first two letters
        # match the generated prefix and the "allocated" field is set to False
        search_criteria = {"identifier": {"$regex": f"^{prefix}"}, "allocated": False}
        matching_record = collection.find_one(search_criteria)

        if matching_record:
            print(f"Creating record: {matching_record['identifier']}")
            # Update the matching_record with new fields
            notion_id = input("Enter Notion ID: ")
            shelf = input("Enter Shelf: ")
            label = input("Enter Label: ")
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
            
            collection.update_one(search_criteria, update_fields)
            print("Record created successfully.")
            print()
            confirmation_query = search_criteria = {"identifier": {matching_record['identifier']}}
            confirmation_record = collection.find(confirmation_query)
            pprint(confirmation_record)
            break
        else:
            print("No matching record found, trying again...")
            attempts += 1
    
    if attempts == max_attempts:
        print(f"After {max_attempts} tries, this script couldn't find an id code available for accessioning. Try running this script again.")