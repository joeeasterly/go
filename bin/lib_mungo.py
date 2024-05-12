#!/usr/local/gh/go/.venv/bin/python3
import sys
import pymongo
def connect_mungo():
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    return collection

def allocate_identifier():
# Connect to mongodb
    collection = connect_mungo()
    # Allocate an identifier for a new record in mongodb
    search_criteria = {"allocated": False}
    filter_criteria = [
        {"$match": search_criteria},
        {"$sample": {"size": 1}}
    ]
    new_record = list(collection.aggregate(filter_criteria))
    selected_record = new_record[0]
    return selected_record

def batch_update():
    # This function essentially works, but it needs to be modified to support multiple kinds of updates.
    collection = connect_mungo()
    documents_to_update = collection.find({})  # You can add a filter here if needed

    for document in documents_to_update:
        identifier = document.get("identifier")
        permalink = f"https://joeeasterly.github.io/go/{identifier}"
        
        # Update the document with the new field using the identifier and add the target field
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"permalink": permalink, "target": "#"}}
        )

def get_last_record():
    """
    Retrieve the most recently updated record in mongodb://mungo/go/link,
    excluding records where "label" is "allocated_by_mungo".
    
    Returns:
        dict: The record with the most recent value in the 'last_updated' field, 
        excluding records with "label" set to "allocated_by_mungo".

    Raises:
        Exception: If no matching records are found in the collection.
    
    Dependencies:
        pymongo
    """
    collection = connect_mungo()
    # Filter to exclude records with "label" set to "allocated_by_mungo"
    filter_criteria = {"label": {"$ne": "allocated_by_mungo"}}
    # Sort by 'last_updated' in descending order and limit the result to the most recent one
    most_recent_record = collection.find(filter_criteria).sort("last_updated", pymongo.DESCENDING).limit(1)
    record = None
    for doc in most_recent_record:  # Since limit is 1, this will iterate once
        record = doc
    if not record:
        raise Exception("No matching records found.")
    return record

def get_record_by_identifier(mungo_id):
    """
    Retrieve a record in mongodb://mungo/go/link by identifier.
    If this script is run directly, mungo_id is passed as a command-line argument.

    Args:
        mungo_id (str): The identifier to search for in the 'identifier' field.

    Returns:
        dict: The record matching the provided identifier.

    Raises:
        Exception: If no record is found matching the provided identifier.
        ValueError: If the provided mungo_id is an empty string.
    
    Dependencies:
        pymongo
        sys
    """
    collection = connect_mungo()
    filter_criteria = {"identifier": mungo_id}
    new_record = collection.find_one(filter_criteria)
    if not new_record:
        raise Exception(f"Identifier {mungo_id} not found.")
    return new_record

def get_storage_record(shcn):
    
    collection = connect_mungo()
    filter_criteria = {"shcn": shcn, "type": "storage"}
    new_record = collection.find_one(filter_criteria)
    if not new_record:
        raise Exception(f"Storage Record {shcn} not found.")
    return new_record

if __name__ == "__main__":
    # mungo_id = sys.argv[1]
    shcn = "10"
    if shcn == "":
        raise ValueError("shcn is required.")
    print(get_storage_record(shcn))

if __name__ == "__main__":
   print("This script is not meant to be run directly.")