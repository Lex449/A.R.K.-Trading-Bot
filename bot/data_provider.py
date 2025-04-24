import finnhub, yfinance as yf, pandas as pd, time
from datetime import datetime

# Finnhub-Client initialisieren (API-Key aus config)
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY) if FINNHUB_API_KEY else None

def get_historical_data(symbol: str):
    """Holt OHLCV-Daten von Finnhub (bei Marktzeiten) oder yfinance (sonst)."""
    now = int(time.time())
    now_utc = datetime.utcnow()
    # Beispiel: Hauptzeiten Mo-Fr von 0-22 Uhr UTC (kann angepasst werden)
    market_open = now_utc.weekday() < 5 and 0 <= now_utc.hour < 22

    if market_open and finnhub_client:
        # Finnhub erwartet Auflösung in Minuten oder 'D' für Tage
        res = INTERVAL
        if res.endswith("h"):
            resolution = str(int(res[:-1])*60)  # z.B. "1h" -> "60"
        elif res.endswith("d"):
            resolution = "D"
        else:
            resolution = res  # weitere Fälle nach Bedarf

        # Zeitraum für Historie (z.B. RSI_PERIOD * 2 Kerzen)
        start_ts = now - RSI_PERIOD * 3600
        resp = finnhub_client.stock_candles(symbol, resolution, start_ts, now)
        if resp.get("s") == "ok":
            df = pd.DataFrame(resp)
            df["t"] = pd.to_datetime(df["t"], unit="s")
            df.set_index("t", inplace=True)
            df.rename(columns={"c": "close"}, inplace=True)
            return df[["close"]]

    # Fallback auf Yahoo Finance (yfinance) außerhalb Hauptzeiten
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="100h", interval=INTERVAL)
    df = df.rename(columns={"Close": "close"})
    return df[["close"]]
