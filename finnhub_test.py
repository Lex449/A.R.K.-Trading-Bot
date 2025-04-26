# finnhub_test.py

import os
import finnhub
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    print("❌ FINNHUB_API_KEY fehlt. Bitte .env überprüfen.")
    exit(1)

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

try:
    symbol = "AAPL"
    res = finnhub_client.quote(symbol)

    if res and res.get("c") not in (None, 0):
        print(f"✅ Erfolgreiche Verbindung. Daten für {symbol}:")
        print(res)
    else:
        print("⚠️ Keine aktuellen Daten erhalten. Markt geschlossen oder Symbol nicht freigeschaltet.")
except Exception as e:
    print(f"❌ Fehler: {e}")
