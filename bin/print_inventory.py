import datetime, os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def split_label(label, max_length):
    """
    Split the label at the last word boundary before max_length.
    Return a tuple with the first line and the remainder.
    """
    if len(label) <= max_length:
        return label, ''
    # Find the last space within the max_length limit
    split_point = label.rfind(' ', 0, max_length)
    if split_point == -1:  # No spaces found, force split at max_length
        return label[:max_length], label[max_length:]
    return label[:split_point], label[split_point+1:]

def print_inventory(record_dict):
    identifier = record_dict.get('identifier', '')
    allocated = record_dict.get('allocated')
    notion_id = record_dict.get('notion_id', '')
    if notion_id is None:
        notion_id = "None"
    bay = record_dict.get('bay', '')
    container = record_dict.get('container', '')
    shelf = record_dict.get('shelf', '')
    slot = record_dict.get('slot', '')
    label = record_dict.get('label', '')
    if label is None:
        label = "(Unallocated)"
    permalink = record_dict.get('permalink', '')
    last_updated = record_dict.get('last_updated')
    inv_class = record_dict.get('class', '')
    inv_type = record_dict.get('type', '')
    location = ' | '.join([str(var) for var in [slot, container, bay, shelf] if var])
    if last_updated is not None:
        last_updated = last_updated.strftime("%Y-%m-%d %H:%M")
    else:
        last_updated = ''
    print("#" * 50)
    
    # Handle label wrapping
    max_label_length = 32  # Max characters for label on the first line
    first_line_label, overflow_label = split_label(label, max_label_length)
    print("Inventory Record: " + first_line_label)
    if overflow_label:
        print(overflow_label.rjust(50))  # Right-align the overflow text
    
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

    # Construct the class, type, and identifier line
    remaining_space = 50 - (len_class + len_type + len_identifier)
    space_between_class_type = remaining_space // 2
    space_between_type_id = remaining_space - space_between_class_type
    class_str = f"Class: {inv_class}"
    type_str = f"Type: {inv_type}"
    id_str = f"Mungo ID: {identifier.upper()}"
    class_type_id = class_str + " " * space_between_class_type + type_str + " " * space_between_type_id + id_str
    print(class_type_id)
    print("#" * 50)
    print()

# Example usage
# if __name__ == "__main__":
    # record_dict = {
    #     'identifier': '12345',
    #     'allocated': True