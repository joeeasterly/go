#!/usr/local/gh/go/.venv/bin/python3                                                                                              
import sys
import pymongo
from pprint import pprint
from lib_git import generate_recset_by_id
from lib_mungo import connect_mungo
def update_record_by_identifier(update_fields, unset_fields=None):
    """
    Update a record in mongodb://mungo/go/link by identifier, using both update and unset fields.

    Args:
        update_fields (dict): A dictionary containing the fields to update.
        unset_fields (dict, optional): A dictionary containing the fields to unset. Defaults to None.

    Raises:
        ValueError: If the identifier is not provided in the update_fields dictionary.
        Exception: If the record with the provided identifier is not found in the collection.

    Returns:
        None
    """
    
    # Check if unset_fields is None and if so, initialize it to an empty dictionary
    if unset_fields is None:
        unset_fields = {}

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

    # Merge update_fields and unset_fields into a single update operation
    update_operation = {**update_fields, **unset_fields}

    # Apply the update
    collection.update_one({"identifier": identifier}, update_operation)
    generate_recset_by_id(identifier)

    # Optionally, print or return a confirmation
    print(f"Record with identifier {identifier} updated successfully.")