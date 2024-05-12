import pymongo
from bson import ObjectId
from datetime import datetime
import json
import os
import subprocess
from lib_mungo import connect_mungo

def git_commit_and_push(directory, file_path, mungo_id):
    """Commit the file to git and push it."""
    try:
        # Move to the repository directory
        os.chdir(directory)

        # Git add the file
        subprocess.check_call(['git', 'add', file_path])

        # Git commit
        commit_message = f'updated identifier {mungo_id}'
        subprocess.check_call(['git', 'commit', '-m', commit_message])

        # Git push
        subprocess.check_call(['git', 'push'])
        print(f'Successfully pushed {file_path} to GitHub.')

    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

def handle_objectid(obj):
    """Handle ObjectId serialization for JSON."""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def push_record(mungo_id):
    """Export MongoDB documents based on a mungo_id to a structured JSON file and commit to GitHub."""
    # Extract the two-character prefix from the mungo_id
    prefix = mungo_id[:2]

    # Initialize MongoDB client and connect to the database
    collection = connect_mungo()

    # Fetch documents whose identifiers start with the prefix
    results = collection.find({"identifier": {'$regex': f'^{prefix}'}})

    # Create a list to hold the documents
    documents_list = []
    for result in results:
        # Convert each document's ObjectId to a string
        result['_id'] = str(result['_id'])
        documents_list.append(result)

    # Define the file path based on the prefix
    first_char = prefix[0]
    second_char = prefix[1]
    file_directory = f'/usr/local/gh/go/data/{first_char}/{second_char}'
    file_path = f'{file_directory}/{prefix}.json'

    # Ensure the directory exists before writing the file
    os.makedirs(file_directory, exist_ok=True)

    # Export the list of documents to a JSON file
    with open(file_path, 'w') as f:
        json.dump(documents_list, f, default=handle_objectid, indent=4)
    
    # Add file to git, commit, and push
    git_commit_and_push(file_directory, file_path, mungo_id)

# Example usage: export_mungo_data('9fau')