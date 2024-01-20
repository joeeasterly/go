from datetime import datetime, date, timedelta
import pymongo

def connect_mongo():
    client = pymongo.MongoClient("mungo:27017")
    db = client["go"]
    collection = db["link"]
    return collection

collection = connect_mongo()

# Get today's date with midnight time
today = datetime.combine(date.today(), datetime.min.time())

# Define the update criteria
update_criteria = {
    'last_updated': {'$gte': today, '$lt': today + timedelta(days=1)},
    'shcn': {'$regex': '^6'}
}

# Define the update operation
update_operation = {
    '$set': {
        'shcn': {'$regex_replace': {'pattern': '^6', 'replacement': '7'}},
        'shelf': {'$regex_replace': {'pattern': '^6', 'replacement': '7'}},
        'bay': {'$regex_replace': {'pattern': '^6', 'replacement': '7'}},
        'container': {'$regex_replace': {'pattern': '^6', 'replacement': '7'}},
        'slot': {'$regex_replace': {'pattern': '^6', 'replacement': '7'}}
    }
}

# Update records based on the criteria
result = collection.update_many(update_criteria, update_operation)

# Print the number of documents updated
print(f'Updated {result.modified_count} documents')