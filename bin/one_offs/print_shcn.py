import pymongo
def connect_mungo():
    client = pymongo.MongoClient("mungo:27017")
    db = client["go"]
    collection = db["link"]
    return collection
collection = connect_mungo()
shcn_list = collection.find({"type": "storage", "shcn": {"$exists": True}, "label": {"$exists": True}})
for shcn in shcn_list:
    print(shcn["shcn"], shcn["label"])