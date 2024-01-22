#!/usr/bin/env python3
import os
import json
from bson import json_util  # Import json_util for ObjectId serialization
from library.connect_mungo import connect_mungo
from library.input_shcn import input_shcn
from library.get_storage_record import get_storage_record

collection = connect_mungo()

# Specify the directory to save the JSON files
output_directory = "/home/joeeasterly/Documents/GitHub/go/shelves"

# Search mungo for records where input_shcn.shcn matches the beginning of the shcn field in the collection.
shelf_list = collection.distinct("shcn")

# Counter for the number of files written
file_counter = 0

# Total number of files
total_files = len(shelf_list)

for shelving_record in shelf_list:
    metadata = get_storage_record(shelving_record)
    if metadata:
        shcn = metadata["shcn"]
        filename = os.path.join(output_directory, f"{shcn.lower()}.json")

        # Create a dictionary for the shelving record
        record_dict = {"shelving_record": json.loads(json.dumps(metadata, default=json_util.default)), "shelf_contents": []}

        shelf_contents = collection.find({"shcn": shcn})

        # Add each item in shelf_contents to the dictionary
        for item in shelf_contents:
            record_dict["shelf_contents"].append(json.loads(json.dumps(item, default=json_util.default)))

        # Write the dictionary to a JSON file
        with open(filename, "w") as json_file:
            json.dump(record_dict, json_file, indent=2, default=json_util.default)

        # Increment the file counter and print the filename to stdout
        file_counter += 1
        print(f"File {file_counter}/{total_files}: {os.path.basename(filename)}")

# The resulting JSON files will be saved in the specified directory (/home/joeeasterly/Documents/GitHub/go/shelves).