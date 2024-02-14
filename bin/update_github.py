#!/usr/bin/env python3
import subprocess
import pymongo
import json
import os
from bson import ObjectId
from datetime import datetime
from connect_mungo import connect_mungo

# Custom JSON encoder to handle serialization of ObjectId and datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ObjectId, datetime)):
            return str(obj)
        return super().default(obj)

# Step 1: Get the most recent commit date from GitHub
commit_date_output = subprocess.check_output(["git", "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M:%S"])
commit_date = commit_date_output.decode("utf-8").strip()

# Convert commit_date string to datetime object
commit_date_datetime = datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S")

# Step 2: Connect to MongoDB
collection = connect_mungo()

# Step 3 and 4: Compare dates and group documents
updated_identifiers = set()
updated_prefixes = set()
for document in collection.find():
    doc_date = document.get("last_updated")  # Replace with the actual date field in your document
    if doc_date is not None:
        if doc_date > commit_date_datetime:
            identifier = document["identifier"]  # Replace with the actual identifier field in your document
            prefix = identifier[:2]
            updated_prefixes.add(prefix)
            updated_identifiers.add(identifier)

# Step 5: Print identifiers
print("Identifiers updated since the most recent GitHub commit:")
for identifier in updated_identifiers:
    print(identifier)
print() # add a line break

# Step 6: Print prefixes
print("Generating JSON files...")
for prefix in updated_prefixes:
    first_letter = prefix[0]
    second_letter = prefix[1]
    # Fetch documents whose identifiers start with the current prefix
    results = collection.find({"identifier": {'$regex': f'^{prefix}'}})

    # Create a list to hold the documents
    documents_list = []

    for result in results:
        # Convert each document's ObjectId to a string
        result['_id'] = str(result['_id'])
        documents_list.append(result)

    # Export the list of documents to a JSON file
    json_file_path = f'/home/joeeasterly/Documents/GitHub/go/data/{first_letter}/{second_letter}/{prefix}.json'
    with open(json_file_path, 'w') as f:
        json.dump(documents_list, f, indent=4, cls=CustomJSONEncoder)
        print(f"Exported {prefix}.json")

    # Step 7: Commit and add the JSON file to Git
    commit_message = f"Add {prefix}.json"  # Customize the commit message

    # Commit the JSON file
    subprocess.run(["git", "add", json_file_path])
    subprocess.run(["git", "commit", "-m", commit_message])

    print(f"Committed and added {prefix}.json to Git")
print() # add a line break
print("JSON files generated and committed to Git successfully. Run `git push` to publish the changes to GitHub.")