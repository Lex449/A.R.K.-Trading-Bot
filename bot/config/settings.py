# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()  # Lokal .env laden, auf Railway ignoriert es das einfach

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY")
    }