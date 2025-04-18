import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY")
    }

# NEU: Frühwarnsystem für ungültige oder fehlende Variablen
def validate_settings():
    settings = get_settings()
    missing = [key for key, value in settings.items() if not value]
    
    if missing:
        print(f"[ERROR] ❌ Fehlende ENV Variablen: {', '.join(missing)}")
        return False
    
    print("[INFO] ✅ Alle ENV Variablen erfolgreich geladen.")
    return True