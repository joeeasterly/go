from datetime import datetime
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
