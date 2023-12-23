#!/usr/bin/env python3
from library.connect_mungo import connect_mungo
from library.input_shcn import input_shcn
collection = connect_mungo()
# Search mungo for records where input_shcn.shcn matches the beginning of the shcn field in the collection.
shcn, shelf, bay, container, slot, analysis = input_shcn()
for record in collection.find({"shcn": {"$regex": "^" + shcn}}):
    print(record["identifier"], record["label"])