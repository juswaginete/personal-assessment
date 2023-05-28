from datetime import datetime

def is_future_or_passed_datetime(datetime):
    current_datetime = datetime.now()

    if datetime > current_datetime or datetime < current_datetime:
        print("The specified datetime is in the future.")
        return False

    return True
