import pymongo
from connect_mungo import connect_mungo

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