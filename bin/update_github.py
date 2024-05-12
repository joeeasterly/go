#!/usr/local/gh/go/.venv/bin/python3
import subprocess
import pymongo
import json
import os
from bson import ObjectId
from datetime import datetime
from lib_mungo import connect_mungo

# Custom JSON encoder for handling ObjectId and datetime serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ObjectId, datetime)):
            return str(obj)
        return super().default(obj)

# Function to fetch the most recent commit date
def get_most_recent_commit_date():
    try:
        commit_date_output = subprocess.check_output(["git", "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M:%S", "--", "data/"])
        commit_date = commit_date_output.decode("utf-8").strip()
        if commit_date:
            return datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S")
        else:
            print("No recent commit data found. Assuming today's date for comparison.")
            return datetime.now()
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch commit date: {e}")
        return datetime.now()  # Fallback to current date

# Main script execution starts here
commit_date_datetime = get_most_recent_commit_date()

# Connect to MongoDB
collection = connect_mungo()

# Compare dates and group documents
updated_identifiers = set()
updated_prefixes = set()
for document in collection.find():
    doc_date = document.get("last_updated")
    if doc_date and doc_date > commit_date_datetime:
        identifier = document["identifier"]
        prefix = identifier[:2]
        updated_prefixes.add(prefix)
        updated_identifiers.add(identifier)

# Print identifiers and process documents
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
    json_file_path = f'/usr/local/gh/go/data/{first_letter}/{second_letter}/{prefix}.json'
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