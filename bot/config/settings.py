import os
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

def get_settings():
    """Lädt alle sensiblen Einstellungen aus der .env-Datei"""
    return {
        "TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_KEY": os.getenv("TWELVEDATA_API_KEY"),
    }