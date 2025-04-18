# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        "TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_KEY": os.getenv("TWELVEDATA_API_KEY")
    }