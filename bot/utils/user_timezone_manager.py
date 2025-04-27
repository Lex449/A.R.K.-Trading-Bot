# bot/utils/user_timezone_manager.py

import json
import os

USER_TIMEZONE_FILE = "user_timezones.json"

def load_user_timezones():
    if os.path.exists(USER_TIMEZONE_FILE):
        with open(USER_TIMEZONE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_user_timezones(data):
    with open(USER_TIMEZONE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def set_user_timezone(chat_id, timezone):
    data = load_user_timezones()
    data[str(chat_id)] = timezone
    save_user_timezones(data)

def get_user_timezone(chat_id):
    data = load_user_timezones()
    return data.get(str(chat_id), "UTC")  # Default UTC if not set
