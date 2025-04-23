import requests
from bot.config import config

def fetch_time_series(symbol: str, interval: str, outputsize: int = 60):
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": config.TWELVEDATA_API_KEY
    }
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        print(f"[FEHLER] Datenabfrage für {symbol} fehlgeschlagen: {e}")
        return None
    if data.get("status") and data["status"] != "ok":
        print(f"[FEHLER] API-Fehler für {symbol}: {data.get('message')}")
        return None
    values = data.get("values")
    if not values:
        print(f"[FEHLER] Keine Daten erhalten für Symbol {symbol}")
        return None
    quotes = []
    for entry in values:
        try:
            quotes.append({
                "datetime": entry["datetime"],
                "open": float(entry["open"]),
                "high": float(entry["high"]),
                "low": float(entry["low"]),
                "close": float(entry["close"])
            })
        except KeyError:
            continue
    quotes.sort(key=lambda x: x["datetime"])
    return quotes
