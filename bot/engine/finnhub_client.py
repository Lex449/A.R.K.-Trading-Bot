# bot/engine/finnhub_client.py

import os
import finnhub
from dotenv import load_dotenv

# .env Variablen laden
load_dotenv()

# API-Key abrufen
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Sicherheit: Validierung, ob API-Key vorhanden ist
if not FINNHUB_API_KEY or FINNHUB_API_KEY.strip() == "":
    raise RuntimeError("❌ FEHLER: FINNHUB_API_KEY fehlt. Bitte in .env oder Railway korrekt setzen.")

# Erzeugt bei jedem Aufruf einen neuen Finnhub Client
def get_finnhub_client() -> finnhub.Client:
    return finnhub.Client(api_key=FINNHUB_API_KEY)
