import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        "TELEGRAM_BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY")
    }