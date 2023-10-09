import pymongo
from print_inventory import print_inventory
from pprint import pprint
def search_records():
    print("Update Record:")
    identifier = input("Enter Identifier (QR Code): ")
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    search_type = ""    
    if "https://joeeasterly.github.io/go/" in identifier:
        identifier = identifier.replace("https://joeeasterly.github.io/go/", "")
        search_type = "identifier"
        filter_criteria = {"identifier": identifier}
    elif len(identifier) == 4:
        search_type = "identifier"
        filter_criteria = {"identifier": identifier}
    elif "inv-" in identifier or "INV-" in identifier:
        search_type = "notion_id"
        identifier = identifier.lower()
        identifier = identifier.replace("inv-", "")
        filter_criteria = {"notion_id": identifier}
    elif "last" in "identifier":
        search_type = "last_updated"
        filter_criteria = { "last_updated": { "$ne": None} }

    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    existing_record = collection.find_one(filter_criteria)
    if existing_record:
        e_all = existing_record.get("allocated")
        e_cla = existing_record.get("class")
        e_ide = existing_record.get("identifier")
        e_lab = existing_record.get("label")
        e_las = existing_record.get("last_updated")
        e_not = existing_record.get("notion_id")
        e_per = existing_record.get("permalink")
        e_she = existing_record.get("shelf")
        e_bay = existing_record.get("bay")
        e_con = existing_record.get("container")
        e_slo = existing_record.get("slot")
        print("Current Record:")
        print(e_ide)
        print(e_lab)
        print("Press J to view full JSON. Press any other key to continue.")
        # After your print statements
        key_input = input().lower()  # Convert to lowercase to ensure both 'J' and 'j' are captured.
        if key_input == 'j':
            pprint(existing_record)  # Pretty print the JSON