from pymongo import MongoClient
from bson import ObjectId
from dateutil.parser import parse

client = MongoClient('mongodb://localhost:27017/')
db = client['go']

# Find all documents with a string type last_updated field
documents = db['link'].find({
    'last_updated': {'$type': 'string'}
})

# Iterate over the documents and update them
for doc in documents:
    try:
        # Parse the string to a datetime object
        updated_date = parse(doc['last_updated'])
        
        # Update the document with the new BSON date type
        db['link'].update_one(
            {'_id': doc['_id']},
            {'$set': {'last_updated': updated_date}}
        )
    except Exception as e:
        print(f"Failed to update document with _id {doc['_id']}: {e}")