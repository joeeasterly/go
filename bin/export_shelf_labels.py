import pymongo
import csv
from datetime import datetime
from connect_mungo import connect_mungo

# MongoDB connection parameters


def get_shelf_list(shcn_prefix):
    """Exports a CSV-formatted list of storage records for label printing."""
    collection = connect_mungo()

    # Use a regular expression for case-insensitive prefix matching
    query = {
        "shcn": {"$regex": f"^{shcn_prefix}", "$options": 'i'}, 
        "type": "storage"
    }
    projection = {"identifier": 1, "permalink": 1, "shcn": 1, "label": 1, "_id": 0}

    return list(collection.find(query, projection))

if __name__ == "__main__":
    shelf_list = []

    while True:
        shcn_prefix = input("Enter SHCN (or '*' to finish): ")
        if shcn_prefix == '*':
            break

        shelf_list.extend(get_shelf_list(shcn_prefix))

    # Save results to CSV file
    if shelf_list:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/usr/local/gh/go/script_out/shelf_list_{timestamp}.csv"

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["identifier", "permalink", "shcn", "label"])
            writer.writeheader()
            writer.writerows(shelf_list)

        print(f"Results saved to '{filename}'")
