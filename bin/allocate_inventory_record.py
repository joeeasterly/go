import pymongo
import random
from library.connect_mungo import connect_mungo

def allocate_inventory_record():
    initials = '123456789abcdefghjkmnopqrstuvwxyz'
    prefix = random.choice(initials) + random.choice(initials)
    collection = connect_mungo()
    matching_record = collection.find_one({"identifier": {"$regex": f"^{prefix}"}, "allocated": False})
    return matching_record