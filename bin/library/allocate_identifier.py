import pymongo

def allocate_identifier():
# Connect to mongodb
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    # Allocate an identifier for a new record in mongodb
    search_criteria = {"allocated": False}
    filter_criteria = [
        {"$match": search_criteria},
        {"$sample": {"size": 1}}
    ]
    new_record = list(collection.aggregate(filter_criteria))
    selected_record = new_record[0]
    return selected_record