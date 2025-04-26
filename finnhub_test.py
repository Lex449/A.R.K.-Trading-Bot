# finnhub_test.py

import os
import finnhub
from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

# API Key laden
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    print("❌ FINNHUB_API_KEY fehlt. Bitte .env prüfen!")
    exit(1)

# Client initialisieren
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

try:
    print("🔍 Starte Test für Symbol: AAPL")
    res = finnhub_client.quote('AAPL')

    if res and res.get("c") not in (None, 0):
        print(f"✅ Erfolgreich: Aktueller Kurs für AAPL: {res['c']}")
    else:
        print("⚠️ Keine aktuellen Daten erhalten (Markt geschlossen oder API-Limit erreicht).")

except Exception as e:
    print(f"❌ Fehler bei der Datenabfrage: {str(e)}")
