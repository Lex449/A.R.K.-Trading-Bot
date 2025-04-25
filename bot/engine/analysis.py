import os
import asyncio
from twelvedata import TDClient
import pandas as pd
import pandas_ta as ta

# Lesen der API-Schlüssel aus Umgebungsvariablen
TD_API_KEY = os.getenv("TWELVEDATA_API_KEY")
if not TD_API_KEY:
    raise ValueError("TWELVEDATA_API_KEY is not set in the environment variables")

# Initialisiere den TwelveData-Client
td = TDClient(apikey=TD_API_KEY)

async def analyze_symbol(symbol: str, lang: str = "en") -> str:
    """
    Führt die technische Analyse für ein gegebenes Symbol durch.
    Berechnet RSI, EMAs, erkennt Chartmuster und erstellt eine Sternebewertung.
    Gibt den Text der Analyse in der gewünschten Sprache zurück.
    """
    # Zeitreihen-Daten abrufen (tägliche Kerzen, 100 Punkte)
    ts = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=100
    ).with_ema(time_period=20).with_ema(time_period=50).with_rsi(time_period=14)
    data = await asyncio.to_thread(ts.as_json)
    # Fehler abfangen
    if not data.get("values"):
        raise Exception(f"Keine Daten für Symbol {symbol}")
    values = data["values"]
    # Neuester Datenpunkt (Absteigend sortiert)
    latest = values[0]
    rsi = float(latest.get("rsi", 0))
    ema20 = float(latest.get("ema_20", 0))
    ema50 = float(latest.get("ema_50", 0))

    # DataFrame für Mustererkennung (aufsteigend sortieren)
    df = pd.DataFrame(values).iloc[::-1].reset_index(drop=True)
    # Chartmuster mit pandas_ta
    hammer = df.ta.cdl_pattern(name="hammer")
    shooting = df.ta.cdl_pattern(name="shootingstar")
    doji = df.ta.cdl_pattern(name="doji")
    last_hammer = hammer.iloc[-1]
    last_shooting = shooting.iloc[-1]
    last_doji = doji.iloc[-1]

    # Seitwärtstrend-Erkennung (falls RSI ~50 und EMAs nahe beieinander)
    sideways = False
    if abs(ema20 - ema50) / (ema50 if ema50 else 1) < 0.02 and 45 < rsi < 55:
        sideways = True
    if last_doji != 0:
        sideways = True

    # Sternebewertung initial (neutral = 3 von 5)
    rating = 3
    if not sideways:
        # RSI-Wertung
        if rsi < 30:
            rating += 1
        elif rsi > 70:
            rating -= 1
        # EMA-Trend
        if ema20 > ema50:
            rating += 1
        else:
            rating -= 1
        # Chartmuster-Wertung
        if last_hammer and last_hammer > 0:
            rating += 1
        if last_shooting and last_shooting > 0:
            rating -= 1
    else:
        rating = 3  # Bei Seitwärtstrend neutral

    rating = max(1, min(rating, 5))
    stars = "★" * rating

    # RSI-Text
    if rsi < 30:
        rsi_text_de, rsi_text_en = "überverkauft", "oversold"
    elif rsi > 70:
        rsi_text_de, rsi_text_en = "überkauft", "overbought"
    else:
        rsi_text_de = rsi_text_en = "neutral"

    # Muster-Text
    if sideways:
        pattern_text_de = "Seitwärtstrend (kein klares Signal)"
        pattern_text_en = "Sideways trend (no clear signal)"
    else:
        if last_hammer and last_hammer > 0:
            pattern_text_de = "Bullischer Hammer"
            pattern_text_en = "Bullish Hammer"
        elif last_shooting and last_shooting > 0:
            pattern_text_de = "Bärischer Stern (Shooting Star)"
            pattern_text_en = "Bearish Star (Shooting Star)"
        else:
            pattern_text_de = "Kein spezifisches Muster"
            pattern_text_en = "No specific pattern"

    # Werte runden
    rsi_val = round(rsi, 2)
    ema20_val = round(ema20, 2)
    ema50_val = round(ema50, 2)

    # Ergebnis-String zusammenstellen
    if lang == "de":
        text = (
            f"Analyse für {symbol}:\n"
            f"RSI: {rsi_val} ({rsi_text_de}), "
            f"EMA20: {ema20_val}, EMA50: {ema50_val}\n"
            f"Muster: {pattern_text_de}\n"
            f"Bewertung: {stars} ({rating}/5 Sterne)"
        )
    else:
        text = (
            f"Analysis for {symbol}:\n"
            f"RSI: {rsi_val} ({rsi_text_en}), "
            f"EMA20: {ema20_val}, EMA50: {ema50_val}\n"
            f"Pattern: {pattern_text_en}\n"
            f"Rating: {stars} ({rating}/5 stars)"
        )
    return text