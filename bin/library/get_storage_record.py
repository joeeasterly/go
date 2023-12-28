#!/usr/bin/env python3
import sys
import pymongo
from library.connect_mungo import connect_mungo
def get_storage_record(shcn):
    
    collection = connect_mungo()
    filter_criteria = {"shcn": shcn, "type": "storage"}
    new_record = collection.find_one(filter_criteria)
    if not new_record:
        raise Exception(f"Storage Record {shcn} not found.")
    return new_record

if __name__ == "__main__":
    # mungo_id = sys.argv[1]
    shcn = "10"
    if shcn == "":
        raise ValueError("shcn is required.")
    print(get_storage_record(shcn))