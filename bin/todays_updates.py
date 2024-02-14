from pymongo import MongoClient
from datetime import datetime, timedelta
from connect_mungo import connect_mungo

# Function to get today's start and end datetime objects
def get_today_start_end():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = start + timedelta(days=1)
    return start, end

# Connect to the MongoDB database
collection = connect_mungo()

# Get today's start and end datetime objects
start_date, end_date = get_today_start_end()

# Query the database, excluding the fields '_id', 'target', 'permalink'
query = {"last_updated": {"$gte": start_date, "$lt": end_date}}
projection = {"_id": 0, "target": 0, "permalink": 0}
cursor = collection.find(query, projection)

# Check if there are any records and if so, print the headers
first_record = cursor.next()
if first_record:
    print("\t".join(first_record.keys()))

    # Reset cursor to the first record
    cursor.rewind()

# Display the records in tab-delimited format
for record in cursor:
    output = []
    for key, value in record.items():
        if key == 'label':
            value = value[:27]  # Trim the 'label' field to 27 characters
        output.append(str(value))
    print("\t".join(output))

# Close the database connection
client.close()