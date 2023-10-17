import pymongo
import sys
from library.print_inventory import print_inventory
from library.parse_qrcode_input import parse_qrcode_input
from library.get_key_press import get_key_press
from pprint import pprint
def search_records():
    print("Search Records:")
    identifier = input("Enter Identifier (QR Code): ")
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    

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
        e_shc = existing_record.get("shcn")
        e_bay = existing_record.get("bay")
        e_con = existing_record.get("container")
        e_slo = existing_record.get("slot")
        print("Current Record:")
        print("ID: " + e_ide)
        print("Label: " + e_lab)
        print("SHCN: "+ e_shc)
        print("Press J to view full JSON. Press any other key to continue.")
        # After your print statements
        key_input = get_key_press()  # Convert to lowercase to ensure both 'J' and 'j' are captured.
        if key_input == 'j':
            print_inventory(existing_record)