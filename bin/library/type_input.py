def type_input(input_string):
    search_type = ""    
    if "https://joeeasterly.github.io/go/" in input_string:
        identifier = input_string.replace("https://joeeasterly.github.io/go/", "")
        search_type = "identifier"
        filter_criteria = {"identifier": input_string}
    elif len(input_string) == 4:
        search_type = "identifier"
        filter_criteria = {"identifier": input_string}
    elif "inv-" in input_string or "INV-" in input_string:
        search_type = "notion_id"
        input_string = input_string.lower()
        input_string = input_string.replace("inv-", "")
        filter_criteria = {"notion_id": input_string}
    elif "last" in input_string:
        search_type = "last_updated"
        filter_criteria = { "last_updated": { "$ne": None} }