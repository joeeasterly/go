import pymongo
def connect_mungo():
    client = pymongo.MongoClient("192.168.86.79:27017")
    db = client["go"]
    collection = db["link"]
    return collection
collection = connect_mungo()
shcn_list = collection.find({"type": "storage", "shcn": {"$exists": True}, "label": {"$exists": True}})
for shcn in shcn_list:
    print(shcn["shcn"], shcn["label"])