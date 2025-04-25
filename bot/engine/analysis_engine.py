# bot/engine/analysis_engine.py

import os
import asyncio
from twelvedata import TDClient

# TwelveData API-Key laden
TD_API_KEY = os.getenv("TWELVEDATA_API_KEY")
if not TD_API_KEY:
    raise ValueError("TWELVEDATA_API_KEY not set in environment variables.")

# TwelveData Client initialisieren
td = TDClient(apikey=TD_API_KEY)

async def fetch_data(symbol: str) -> list:
    """Holt historische Kursdaten für ein Symbol."""
    try:
        series = td.time_series(
            symbol=symbol,
            interval="1min",
            outputsize=50
        ).as_json()
        return series.get("values", [])
    except Exception as e:
        print(f"[ERROR] Data fetch failed for {symbol}: {e}")
        return []

async def analyze_symbol(symbol: str, lang: str = "en") -> str:
    """Analysiert ein Symbol und gibt ein Rating + Analyse-Text zurück."""
    data = await asyncio.to_thread(fetch_data, symbol)
    if not data or len(data) < 20:
        return f"❌ No sufficient data for {symbol}."

    # Neueste Datenpunkte
    closes = [float(entry["close"]) for entry in reversed(data)]

    # RSI berechnen
    rsi = calculate_rsi(closes)
    # EMAs berechnen
    ema_short = calculate_ema(closes, period=9)
    ema_long = calculate_ema(closes, period=21)

    # Trend erkennen
    trend = detect_trend(ema_short, ema_long)

    # Seitwärtstrend erkennen
    sideways = detect_sideways(closes)

    # Sterne-Bewertung erstellen
    stars = generate_stars(rsi, trend, sideways)

    # Analyse-Text erzeugen
    return format_analysis(symbol, rsi, ema_short, ema_long, trend, stars, lang)

def calculate_rsi(prices: list, period: int = 14) -> float:
    """Berechnet den RSI eines Preisverlaufs."""
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def calculate_ema(prices: list, period: int) -> float:
    """Berechnet den EMA eines Preisverlaufs."""
    ema = sum(prices[:period]) / period
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return round(ema, 2)

def detect_trend(ema_short: float, ema_long: float) -> str:
    """Erkennt Trend basierend auf EMA-Schnittpunkten."""
    if ema_short > ema_long:
        return "up"
    elif ema_short < ema_long:
        return "down"
    return "neutral"

def detect_sideways(prices: list, threshold: float = 0.01) -> bool:
    """Erkennt einen Seitwärtstrend basierend auf Preisabweichungen."""
    min_price = min(prices[-20:])
    max_price = max(prices[-20:])
    return (max_price - min_price) / min_price < threshold

def generate_stars(rsi: float, trend: str, sideways: bool) -> int:
    """Generiert eine Sternebewertung basierend auf RSI, Trend und Seitwärtsbewegung."""
    stars = 3
    if sideways:
        return stars
    if trend == "up":
        stars += 1
    elif trend == "down":
        stars -= 1
    if rsi < 30:
        stars += 1
    elif rsi > 70:
        stars -= 1
    return min(max(stars, 1), 5)

def format_analysis(symbol: str, rsi: float, ema_short: float, ema_long: float, trend: str, stars: int, lang: str) -> str:
    """Formatiert die Analyse-Ausgabe abhängig von Sprache."""
    trend_text = {
        "up": {"de": "steigender Trend", "en": "uptrend"},
        "down": {"de": "fallender Trend", "en": "downtrend"},
        "neutral": {"de": "neutraler Trend", "en": "neutral trend"}
    }
    star_str = "★" * stars + "☆" * (5 - stars)

    if lang == "de":
        return (
            f"Analyse für {symbol}:\n"
            f"RSI: {rsi}\n"
            f"EMA(9): {ema_short} | EMA(21): {ema_long}\n"
            f"Trend: {trend_text[trend]['de']}\n"
            f"Bewertung: {star_str} ({stars}/5)"
        )
    else:
        return (
            f"Analysis for {symbol}:\n"
            f"RSI: {rsi}\n"
            f"EMA(9): {ema_short} | EMA(21): {ema_long}\n"
            f"Trend: {trend_text[trend]['en']}\n"
            f"Rating: {star_str} ({stars}/5)"
        )
