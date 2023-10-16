import datetime, os
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def print_inventory(record_dict):
    identifier = record_dict.get('identifier', '')
    allocated = record_dict.get('allocated')
    notion_id = record_dict.get('notion_id', '')
    bay = record_dict.get('bay', '')
    container = record_dict.get('container', '')
    shelf = record_dict.get('shelf', '')
    slot = record_dict.get('slot', '')
    label = record_dict.get('label', '')
    permalink = record_dict.get('permalink', '')
    last_updated = record_dict.get('last_updated')
    inv_class = record_dict.get('class', '')
    inv_type = record_dict.get('type', '')
    location = ' | '.join([str(var) for var in [slot, container, bay, shelf] if var])
    if last_updated is not None:
        last_updated = last_updated.strftime("%Y-%m-%d %H:%M")
    else:
        last_updated = ''
    clear()
    print("Inventory Record: " + label)
    len_location = len("SHCN: " + location)
    len_notion = len("Notion : " + notion_id)
    loc_notion_spacing = 50 - (len_location + len_notion)
    len_last_updated = len("Last Updated: " + last_updated)
    len_allocated = len("Allocated: " + str(allocated))
    len_allocated_spacing = 50 - (len_last_updated + len_allocated)
    print("SHCN: " + location + " " * loc_notion_spacing + "Notion: " + notion_id)
    print("Last Updated: " + last_updated + " " * len_allocated_spacing + "Allocated: " + str(allocated))
    len_class = len("Class: " + inv_class)
    len_type = len("Type: " + inv_type)
    len_identifier = len("Mungo ID: " + identifier)
    len_id_spacing = 50 - (len_class + len_type + len_identifier)
    print("Class/Type: " + inv_class + "/" + inv_type)

# Run the update_record function if this script is run directly
# if __name__ == "__main__":
    # print(print_inventory(record_dict))