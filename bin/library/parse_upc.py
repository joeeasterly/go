def parse_upc(existing_upc = None):
    permitted_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    upc_prompt = "Enter UPC: "
    if existing_upc:
        upc_prompt = f"Enter UPC [{existing_upc}]: "
    upc = input(upc_prompt)
    if not upc:
        upc = existing_upc
    # Remove all characters in the label except those in the permitted_characters list.
    upc = "".join([character for character in upc if character in permitted_characters])
    return upc