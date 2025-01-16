import re
from datetime import datetime

def human_readable_size(size_in_bytes: int) -> str:
    """
    Convert file size from bytes to a human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"

def is_valid_file(filename: str, allowed_extensions: list) -> bool:
    """
    Check if a file has a valid extension.
    """
    return filename.split('.')[-1].lower() in allowed_extensions

def sanitize_file_name(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    """
    return re.sub(r'[^\w\-_. ]', '_', filename)

def log_event(event_message: str) -> None:
    """
    Log an event with a timestamp.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {event_message}")

def paginate_list(items: list, page: int, items_per_page: int) -> list:
    """
    Paginate a list of items.
    """
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end]

def format_message(title: str, size: int, file_id: str) -> str:
    """
    Format a message for sending filtered file details.
    """
    size_str = human_readable_size(size)
    return f"**Title:** {title}\n**Size:** {size_str}\n**File ID:** `{file_id}`"

def extract_keywords(text: str) -> list:
    """
    Extract keywords from a given text for filtering purposes.
    """
    return [word.strip().lower() for word in text.split() if len(word) > 2]
  
