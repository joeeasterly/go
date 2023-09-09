import pymongo
from pprint import pprint
from datetime import datetime
from link_notion_inventory import link_notion_inventory
from print_inventory import print_inventory

def update_record():
    print("Update Record:")
    
    identifier = input("Enter Identifier (QR Code): ")
    
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    
    filter_criteria = {"identifier": identifier}
    existing_record = collection.find_one(filter_criteria)
    
    if existing_record:
        print("Current Record:")
        print_inventory(existing_record, "label", "identifier", "notion_id", "shelf")
        print("JSON:")
        pprint(existing_record)
        
        notion_id = input(f"Enter Notion ID (INV-) [{existing_record.get('notion_id')}]: ")
        shelf = input(f"Enter Shelf Number [{existing_record.get('shelf')}]: ")
        label = input(f"Enter Label [{existing_record.get('label')}]: ")
        
        update_data = {
            "$set": {
                "notion_id": notion_id if notion_id else existing_record.get("notion_id"),
                "shelf": shelf if shelf else existing_record.get("shelf"),
                "label": label if label else existing_record.get("label"),
                "last_updated": datetime.now()
            }
        }
        
        result = collection.update_one(filter_criteria, update_data)
        
        if result.matched_count > 0:
            updated_record = collection.find_one(filter_criteria)
            print("Record updated successfully!")
            print()
            print_inventory(updated_record, "label", "identifier", "notion_id", "shelf")
            print("JSON:")
            pprint(updated_record)
            # If notion_id is provided, call the update_notion_record function
            if notion_id:
                update_result = link_notion_inventory(notion_id, identifier)
                print(update_result)
        else:
            print("No record found with the provided identifier.")
    else:
        print("No record found with the provided identifier.")