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
        input_shelf = input(f"Enter Shelving Location [{existing_record.get('shelf')}]: ")
        shelf_length = len(input_shelf)
        if shelf_length == 1:
            raise ValueError("Location must between two and five hex digits.")
        if shelf_length >= 2:
            shelf = input_shelf[:2]
        if shelf_length >= 3:
            bay = input_shelf[:3]
        if shelf_length >= 4:
            container = input_shelf[:4]
        if shelf_length >= 5:
            slot = input_shelf[:5]
        if shelf_length >= 6:
            raise ValueError("Location must between two and five hex digits.")


        label = input(f"Enter Label [{existing_record.get('label')}]: ")
        
        update_data = {
            "$set": {
                "notion_id": notion_id if notion_id else existing_record.get("notion_id"),
                "shelf": shelf if shelf else existing_record.get("shelf"),
                "bay": bay if bay else existing_record.get("bay"),
                "container": container if container else existing_record.get("container"),
                "slot": slot if slot else existing_record.get("slot"),
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