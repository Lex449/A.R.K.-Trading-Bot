import os

# Liefert alle wichtigen Variablen aus Railway-Umgebung zurück
def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY")
    }