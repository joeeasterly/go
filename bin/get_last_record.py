#!/usr/bin/env python3
import sys
import pymongo
from connect_mungo import connect_mungo

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

if __name__ == "__main__":
    try:
        print(get_last_record())
    except Exception as e:
        print(f"Error: {e}")