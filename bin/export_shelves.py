#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime
from bson import json_util
import subprocess  # Import subprocess
from connect_mungo import connect_mungo
from parse_shcn_input import parse_shcn_input
from get_storage_record import get_storage_record

collection = connect_mungo()

# Specify the directory to save the JSON files
output_directory = "/home/joeeasterly/Documents/GitHub/go/shelves/data"

# Specify the path to the Git repository
repo_path = "/home/joeeasterly/Documents/GitHub/go/shelves"

# Search mungo for records where parse_shcn_input.shcn matches the beginning of the shcn field in the collection.
shelf_list = collection.distinct("shcn")

# Counter for the number of files written
file_counter = 0

# Total number of files
total_files = len(shelf_list)
# Set the commit message for the shelves
commit_message = f"shelves update {datetime.now()}"

for shelving_record in shelf_list:
    metadata = get_storage_record(shelving_record)
    if metadata:
        shcn = metadata["shcn"]
        identifier = metadata["identifier"]
        filename = f"{shcn.lower()}.json"  # Update to use lowercase shcn for consistency

        # Check if shcn has a non-zero length before accessing its first character
        if shcn:
            subfolder = shcn[0]  # Get the first character of shcn for subfolder

            # Create the subfolder if it doesn't exist
            subfolder_path = os.path.join(output_directory, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)

            # Create a dictionary for the shelving record
            record_dict = {"shelving_record": json.loads(json.dumps(metadata, default=json_util.default)), "shelf_contents": []}

            shelf_contents = collection.find({"shcn": {"$regex": f"^{re.escape(shcn)}[a-zA-Z0-9]{{0,2}}$"}, "identifier": {"$ne": identifier}})

            # Add each item in shelf_contents to the dictionary
            for item in shelf_contents:
                record_dict["shelf_contents"].append(json.loads(json.dumps(item, default=json_util.default)))

            # Write the dictionary to a JSON file in the subfolder
            with open(os.path.join(subfolder_path, filename), "w") as json_file:
                json.dump(record_dict, json_file, indent=2, default=json_util.default)

            # Increment the file counter and print the filename to stdout
            file_counter += 1
            print(f"File {file_counter}/{total_files}: {os.path.join(subfolder, filename)}")

# Use subprocess to stage, commit, and push changes
subprocess.run(["git", "add", "."], cwd=repo_path)
subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path)
print("Shelves updated. Run git push to push changes to GitHub.")