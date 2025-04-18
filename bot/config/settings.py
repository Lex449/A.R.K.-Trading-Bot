import os
from dotenv import load_dotenv

load_dotenv()  # Lokal nutzbar – auf Railway hat keine Wirkung, aber safe fallback

def get_settings():
    required_keys = ["BOT_TOKEN", "DANIEL_TELEGRAM_ID", "TWELVEDATA_API_KEY"]
    settings = {}

    for key in required_keys:
        value = os.getenv(key)
        if not value:
            raise EnvironmentError(f"{key}")
        settings[key] = value

    return settings