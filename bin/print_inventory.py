def print_inventory(record_dict, *fields):
    output_lines = []
    for field in fields:
        field_value = record_dict.get(field, "N/A")
        formatted_field = f"{field.title()}: {field_value}"
        output_lines.append(formatted_field)
    return "\n".join(output_lines)