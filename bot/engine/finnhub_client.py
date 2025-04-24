# bot/engine/finnhub_client.py

import os
import finnhub

# === API-Key laden ===
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# === Fehler bei fehlendem Key verhindern ===
if not FINNHUB_API_KEY:
    raise ValueError("❌ FINNHUB_API_KEY fehlt. Bitte in .env oder Railway setzen!")

# === Finnhub-Client initialisieren ===
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
