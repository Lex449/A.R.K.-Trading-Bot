import os
import finnhub
from dotenv import load_dotenv

# .env Variablen laden
load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Validierung
if not FINNHUB_API_KEY:
    raise ValueError("❌ FINNHUB_API_KEY fehlt! Bitte in .env oder Railway eintragen.")

# Rückgabe eines neuen Finnhub Clients bei jedem Aufruf
def get_finnhub_client():
    return finnhub.Client(api_key=FINNHUB_API_KEY)
