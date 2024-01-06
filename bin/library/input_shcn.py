def input_shcn(existing_shcn = None):
    # clear the variables
    shcn = shelf = bay = container = slot = analysis = None
    
    # Prompt the user to enter an SHCN
    shcn_prompt = "Enter SHCN: "
    if existing_shcn:
        shcn_prompt = f"Enter SHCN [{existing_shcn}]: "
    shcn = input(f"Enter SHCN: ").upper()
    # If the the user does not enter an SHCN, use the existing SHCN instead.
    if not shcn:
        shcn = existing_shcn
    
    # Parse out the shelf, bay, container, and slot from the SHCN.
    shcn_length = len(shcn)
    if shcn_length < 2 or shcn_length >= 38:
        raise ValueError("Input must be either a 2-5 hex digit SHCN, a 4-digit identifier, or a qrcode URL")
    if shcn_length >= 2:
        shelf = shcn[:2]
        analysis = "Shelf: " + shelf
    if shcn_length >= 3:
        bay = shcn[:3]
        analysis = analysis + ", Bay: " + bay
    if shcn_length >= 4:
        container = shcn[:4]
        analysis = analysis + ", Container: " + container
    if shcn_length >= 5:
        slot = shcn[:5]
        analysis = analysis + ", Slot: " + slot
        
    return shcn, shelf, bay, container, slot, analysis