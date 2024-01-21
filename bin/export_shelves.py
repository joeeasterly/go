#!/usr/bin/env python3
from library.connect_mungo import connect_mungo
from library.input_shcn import input_shcn
from library.get_storage_record import get_storage_record
collection = connect_mungo()
# Search mungo for records where input_shcn.shcn matches the beginning of the shcn field in the collection.

shelf_list = collection.distinct("shcn")
for shelving_record in shelf_list:
    metadata = get_storage_record(shelving_record)
    if metadata:
        label = metadata["label"]
        shcn = metadata["shcn"]
        print(shcn, label)
        shelf_contents = collection.find({"shcn": shcn})
        for item in shelf_contents:
            print(" --", item["identifier"], item["label"])

# shcn, shelf, bay, container, slot, analysis = input_shcn()
# for record in collection.find({"shcn": {"$regex": "^" + shcn}}):
#     print(record["identifier"], record["label"])