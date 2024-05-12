#!/usr/local/gh/go/.venv/bin/python3
from pymongo import MongoClient
import csv
import bson
from library.connect_mungo import connect_mungo

# MongoDB Connection
collection = connect_mungo()

# Excluded fields from update
excluded_fields = ["some_field1", "some_field2"]

# Read CSV and Update MongoDB
with open("/usr/local/gh/go/bin/one_offs/20231019_storage_fix.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = {"_id": bson.ObjectId(row["_id"])}  # Matching by _id, converting to ObjectId
        update_fields = {k: row[k] for k in row.keys() if k not in excluded_fields and k != "_id"}  # Excluding fields
        
        update_query = {"$set": update_fields}
        
        # Update record in MongoDB
        collection.update_one(query, update_query)

print("Update process completed.")