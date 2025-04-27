from datetime import datetime


def convert_date(date_string: str, target_format: str = "timestamp"):
    # Convert to a datetime object
    datetime_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if target_format == "timestamp":
        # Convert to a timestamp
        timestamp = datetime_obj.timestamp()
        return timestamp
    if target_format == "datetime":
        date_obj = datetime_obj.date()
        return date_obj

    return None
