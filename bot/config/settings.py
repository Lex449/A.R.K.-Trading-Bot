# bot/config/settings.py

import os
from dotenv import load_dotenv

# Lädt die .env-Datei automatisch beim Start
load_dotenv()

def get_settings():
    return {
        "TOKEN": os.getenv("BOT_TOKEN"),  # Telegram Bot Token
        "DANIEL_ID": os.getenv("DANIEL_TELEGRAM_ID"),  # Deine Telegram-ID
        "TWELVEDATA_KEY": os.getenv("TWELVEDATA_API_KEY")  # API-Key für Marktanalyse
    }