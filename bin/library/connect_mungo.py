import pymongo
def connect_mungo():
    client = pymongo.MongoClient("mungo:27017")
    db = client["go"]
    collection = db["link"]
    return collection