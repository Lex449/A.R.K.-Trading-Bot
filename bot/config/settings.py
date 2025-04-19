import os
from dotenv import load_dotenv

load_dotenv()  # Lädt die .env-Datei

def get_settings():
    return {
        "TOKEN": os.getenv("BOT_TOKEN"),  # Hier wird der Token aus der .env-Datei geladen
        "DANIEL_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_KEY": os.getenv("TWELVEDATA_API_KEY")
    }