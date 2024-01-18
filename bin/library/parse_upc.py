def parse_upc(existing_upc = None):
    import pymongo
    from library.connect_mungo import connect_mungo
    permitted_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    upc_prompt = "Enter UPC: "
    upc = ""
    if existing_upc:
        upc_prompt = f"Enter UPC [{existing_upc}]: "
    upc = input(upc_prompt)
    if upc:
        # Remove all characters in the label except those in the permitted_characters list.
        upc = "".join([character for character in upc if character in permitted_characters])
        collection = connect_mungo()
        filter_criteria = {"upc": upc}
        existing_record = collection.find_one(filter_criteria)
        if existing_record:
            upc_label = existing_record.get("label")
        else:
            upc_label = None
    if not upc:
        upc = existing_upc
    return upc, upc_label