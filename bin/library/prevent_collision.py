import pymongo
def prevent_collision(shcn):
    # make sure that the SHCN is not already an allocated mungo id
    shcn = shcn.replace("https://joeeasterly.github.io/go/", "")
    shcn_length = len(shcn)
    if shcn_length == 4:
        client = pymongo.MongoClient("mungo.local:27017")
        db = client["go"]
        collection = db["link"]
        filter_criteria = {"identifier": shcn}
        existing_record = collection.find_one(filter_criteria)
        if existing_record:
            allocated = existing_record.get('allocated')
            if allocated:
                raise ValueError(f"Warning: identifier/shcn collision: " + shcn + ". Fix it first in mongodb compass and try again.")
    return shcn