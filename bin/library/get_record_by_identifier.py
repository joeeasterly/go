#!/usr/bin/env python3
import sys
import pymongo
from library.connect_mungo import connect_mungo
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

if __name__ == "__main__":
    # mungo_id = sys.argv[1]
    mungo_id = "af8f"
    if mungo_id == "":
        raise ValueError("mungo id is required.")
    print(get_record_by_identifier(mungo_id))