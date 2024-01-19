from pymongo import MongoClient
from datetime import datetime
import csv
from library.connect_mungo import connect_mungo

try:
    # Get the number of records to allocate from user input and validate
    size = int(input("How many records would you like to allocate? "))
    if size < 1:
        size = 1
except ValueError:
    print("Invalid input. Setting the number of records to 1.")
    size = 1

# Connect to MongoDB
collection = connect_mungo()

# Define the aggregation pipeline
pipeline = [
    {
        "$match": {
            "allocated": False,
            "staged": {"$exists": False}
        }
    },
    {
        "$sample": {"size": size}
    }
]

# Execute the aggregation
random_docs = list(collection.aggregate(pipeline))

# Initialize the identifiers list
identifiers = []

# Check if any documents were found
if random_docs:
    for chosen_record in random_docs:
        # Get the value of the 'identifier' field
        identifier_value = chosen_record.get("identifier", None).upper()
        permalink = chosen_record.get("permalink", None)

        # Update that record by setting the 'staged' field to the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        collection.update_one({"_id": chosen_record["_id"]}, {"$set": {"staged": current_time}})

        # Add data to the 'identifiers' list
        identifiers.append({"identifier": identifier_value, "permalink": permalink, "staged": current_time})

    # Get today's date
    today_date = datetime.now().strftime("%Y%m%d")

    # Write the identifiers to a CSV file
    with open(f"/home/joeeasterly/Documents/GitHub/go/script_out/qrcodes_{today_date}.csv", "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["identifier", "permalink", "staged"])

        # Write the header if the file is new
        if f.tell() == 0:
            writer.writeheader()

        for record in identifiers:
            writer.writerow(record)
else:
    print("No eligible records found.")