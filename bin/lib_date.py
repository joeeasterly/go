from datetime import datetime
from datetime import datetime
from dateparser import parse
def read_mongodb_date(record, field):
    """Reads a date from a MongoDB record and returns it as an ISO formatted string.

    Args:
        record: A MongoDB record.
        field: The name of the field containing the date.

    Returns:
        The date as an ISO formatted string, or None if the date is not found or is not
        a valid date.
    """

    date_value = record.get(field)
    if date_value:
        if isinstance(date_value, datetime):  # Handle datetime objects directly
            return date_value.isoformat()
        elif isinstance(date_value, str):  # Handle date strings 
            try:
                dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")  # Adjust format if needed
                return dt.isoformat()
            except ValueError:
                pass  # Ignore invalid date strings
    return None

def parse_date_input(existing_record, last_record, date_field, message=None):
    if message is None:
        message = "Enter date (YYYYMMDD or + to use last record's date, leave blank to use existing date): "
    
    existing_date = read_mongodb_date(existing_record, date_field)
    last_date = read_mongodb_date(last_record, date_field)

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