"""
A.R.K. User Timezone Manager – Handles individual user timezones.
"""

import json
import os
from pytz import all_timezones

USER_TIMEZONE_FILE = "user_timezones.json"

def load_user_timezones():
    if os.path.exists(USER_TIMEZONE_FILE):
        with open(USER_TIMEZONE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_user_timezones(data):
    with open(USER_TIMEZONE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    if timezone not in all_timezones:
        return False
    data = load_user_timezones()
    data[str(chat_id)] = timezone
    save_user_timezones(data)
    return True

def get_user_timezone(chat_id: int) -> str:
    data = load_user_timezones()
    return data.get(str(chat_id), "UTC")  # Default fallback: UTC

def list_available_timezones() -> list:
    return all_timezones
