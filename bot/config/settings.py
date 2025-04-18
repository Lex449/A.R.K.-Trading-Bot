import os
from dotenv import load_dotenv
load_dotenv()

# Diese Funktion prüft, ob alle ENV-Variablen gesetzt sind.
def get_settings():
    required_keys = ["BOT_TOKEN", "DANIEL_TELEGRAM_ID", "TWELVEDATA_API_KEY"]
    settings = {}

    for key in required_keys:
        value = os.getenv(key)
        if not value:
            raise EnvironmentError(f"❌ Fehlende Umgebungsvariable: {key}")
        settings[key] = value

    return settings