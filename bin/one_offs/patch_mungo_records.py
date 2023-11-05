from pymongo import MongoClient
import csv
import bson

# MongoDB Connection
client = MongoClient("mongodb://mungo.local:27017/")
db = client['go']
collection = db['link']

# Excluded fields from update
excluded_fields = ["some_field1", "some_field2"]

# Read CSV and Update MongoDB
with open("/home/joeeasterly/Documents/GitHub/go/bin/one_offs/20231019_storage_fix.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = {"_id": bson.ObjectId(row["_id"])}  # Matching by _id, converting to ObjectId
        update_fields = {k: row[k] for k in row.keys() if k not in excluded_fields and k != "_id"}  # Excluding fields
        
        update_query = {"$set": update_fields}
        
        # Update record in MongoDB
        collection.update_one(query, update_query)

print("Update process completed.")