from pymongo import MongoClient
from datetime import datetime

# Connect to the MongoDB server
client = MongoClient('mungo:27017')
db = client.go

# Step 2: Retrieve distinct "upc" values from the "link" collection
distinct_upcs = db.link.distinct("upc")

# Step 4: Iterate through distinct "upc" values
for upc in distinct_upcs:
    # Step 3: Retrieve the corresponding "label" values
    label = db.link.find_one({"upc": upc})["label"]
    
    # Step 5: Create a document with required fields
    document = {
        "identifier": upc,
        "label": label,
        "type": "upc",
        "last_updated": datetime.utcnow(),
        "source": "object"
    }

    # Step 6: Insert the document into the "identifiers" collection
    db.identifiers.insert_one(document)

# Close the MongoDB connection
client.close()