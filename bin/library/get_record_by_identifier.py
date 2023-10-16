import pymongo
def get_record_by_identifier(mungo_id):
    client = pymongo.MongoClient("mungo.local:27017")
    db = client["go"]
    collection = db["link"]
    filter_criteria = {"identifier": mungo_id}
    new_record = collection.find_one(filter_criteria)
    if not new_record:
        raise Exception(f"Identifier {mungo_id} not found.")
    return new_record