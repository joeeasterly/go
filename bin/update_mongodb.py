#!/usr/bin/env python3
import pymongo

# MongoDB connection settings
client = pymongo.MongoClient("mungo.local:27017")  # Update connection URL as needed
database = client["go"]
collection = database["link"]

# Update documents in the collection
def update_documents():
    documents_to_update = collection.find({})  # You can add a filter here if needed

    for document in documents_to_update:
        identifier = document.get("identifier")
        permalink = f"https://joeeasterly.github.io/go/{identifier}"
        
        # Update the document with the new field using the identifier and add the target field
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"permalink": permalink, "target": "#"}}
        )

if __name__ == "__main__":
    update_documents()
    print("Records updated successfully.")
