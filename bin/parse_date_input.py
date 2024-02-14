from datetime import datetime
from dateparser import parse

def get_mongodb_date_as_string(record, field):
    mongodb_date = record.get(field)
    if mongodb_date and isinstance(mongodb_date, dict):  # Check for nested structure
        date_str = mongodb_date.get("$date")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")  # Parse ISO Format
            return dt.isoformat()
        else:
            return None
    else:
        return None

def parse_date_input(existing_record, last_record, date_field, message=None):
    if message is None:
        message = "Enter date (YYYYMMDD or + to use last record's date, leave blank to use existing date): "
    
    existing_date = get_mongodb_date_as_string(existing_record, date_field)
    last_date = get_mongodb_date_as_string(last_record, date_field)

    input_date = input(message).strip()  # Strip to remove leading/trailing whitespace

    if input_date == "":
        # User hits return without input, use the existing date if it exists, or None if it doesn't
        return existing_date if existing_date else None
    elif input_date == "+":
        # User enters "+", use the date from the last_record
        return last_date
    else:
        # User enters a date, parse it
        if input_date.isdigit() and len(input_date) == 8:
            # If input is eight consecutive digits, parse as YYYYMMDD
            output_date = parse(input_date, date_formats=["%Y%m%d"])
        else:
            # Otherwise, use dateparser to parse any recognizable date format
            output_date = parse(input_date)
        return output_date.isoformat() if output_date else None

# Note: The above implementation assumes that `get_mongodb_date_as_string` returns an ISO formatted date string
# and that existing_date and last_date are in the correct format to be directly returned if chosen.