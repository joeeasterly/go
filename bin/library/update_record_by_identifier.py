#!/usr/bin/env python3
import sys
import pymongo
from pprint import pprint
from library.connect_mungo import connect_mungo
def update_record_by_identifier(update_fields):
    """
    Update a record in mongodb://mungo/go/link by identifier.
    If this script is run directly, the update_fields dictionary is passed as a command-line argument.

    Args:
        update_fields (dict): A dictionary containing the fields to update and the identifier of the record to update.

    Raises:
        ValueError: If the identifier is not provided in the update_fields dictionary.
        Exception: If the record with the provided identifier is not found in the collection.

    Returns:
        None
    Dependencies:
        pymongo
        sys
    """
    
    # Extract the identifier from the update_fields dictionary
    identifier = update_fields.get('$set', {}).get('identifier', None)
    if identifier is None:
        raise ValueError("identifier is required in update_fields.")

    # Initialize MongoDB client and collection
    collection = connect_mungo()

    # Fetch the record by identifier
    filter_criteria = {"identifier": identifier}
    existing_record = collection.find_one(filter_criteria)
    if not existing_record:
        raise Exception(f"Identifier {identifier} not found.")

    # Apply the update
    collection.update_one({"identifier": identifier}, update_fields)

    # Optionally, print or return a confirmation
    print(f"Record with identifier {identifier} updated successfully.")
if __name__ == "__main__":
    import sys
    update_fields = sys.argv[1]
    if update_fields == "":
        raise ValueError("update_fields dictionary is required.")
    update_record_by_identifier(update_fields)