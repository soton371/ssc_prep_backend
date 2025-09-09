from datetime import datetime


#utility function to get current month name e.g., "September"
def current_month() -> str:
    return datetime.now().strftime("%B")  # e.g., "September"

