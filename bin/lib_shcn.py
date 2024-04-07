from lib_mungo import get_record_by_identifier

def parse_shcn_input(existing_shcn=None, last_record=None, message=None):
    if last_record is None:
        last_record = {}  # Create a new dictionary if none was provided
    last_shcn = last_record.get('shcn', None)
    shcn = shelf = bay = container = slot = analysis = None
    if message is not None:
        shcn_prompt = message
    else:
        shcn_prompt = f"Enter SHCN [{existing_shcn}]: " if existing_shcn else "Enter SHCN: "
    shcn = input(shcn_prompt)
    
    if not shcn:
        shcn = existing_shcn
    
    if shcn.startswith("https://joeeasterly.github.io"):
        mungo_id = shcn.split("/")[-1]
        record = get_record_by_identifier(mungo_id)
        if record:
            shcn = record.get('shcn', '')
        else:
            raise ValueError("No record found for the given Mungo ID")
    
    shcn_length = len(shcn)
    if shcn_length < 2 or shcn_length > 5:
        if shcn == "+":
            shcn = last_shcn
        else:
            raise ValueError("SHCN must be between 2 and 5 characters")

    # Parsing logic corrected based on the SHCN length
    if shcn_length >= 2:
        shelf = shcn[:2].upper()
    if shcn_length >= 3:
        bay = shcn[:3].upper()
    if shcn_length == 4:
        container = shcn.upper()
    elif shcn_length == 5:
        container = shcn[:4].upper()
        slot = shcn.upper()
    
    # Building the analysis string based on available data
    analysis = "Shelf: " + (shelf if shelf else "")
    if bay:
        analysis += ", Bay: " + bay
    if container:
        analysis += ", Container: " + container
    if slot:
        analysis += ", Slot: " + slot

    return shcn.upper(), shelf, bay, container, slot, analysis