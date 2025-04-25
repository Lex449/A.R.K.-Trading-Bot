# bot/engine/analysis_engine.py

import os
import asyncio
from twelvedata import TDClient
from bot.config.settings import get_settings

settings = get_settings()

TD_API_KEY = settings["TWELVEDATA_API_KEY"]
if not TD_API_KEY:
    raise ValueError("TWELVEDATA_API_KEY is missing.")

td = TDClient(apikey=TD_API_KEY)

async def fetch_data(symbol: str) -> list:
    """Holt historische Kursdaten von TwelveData."""
    try:
        series = td.time_series(
            symbol=symbol,
            interval=settings["INTERVAL"],
            outputsize=50
        ).as_json()
        return series.get("values", [])
    except Exception as e:
        print(f"[ERROR] Data fetch failed for {symbol}: {e}")
        return []

async def analyze_symbol(symbol: str, lang: str = "en") -> str:
    """Analysiert ein Symbol und gibt ein Text-Rating zurück."""
    data = await asyncio.to_thread(fetch_data, symbol)
    if not data or len(data) < 20:
        return f"❌ No sufficient data for {symbol}."

    closes = [float(entry["close"]) for entry in reversed(data)]
    rsi = calculate_rsi(closes)
    ema_short = calculate_ema(closes, period=settings["EMA_SHORT_PERIOD"])
    ema_long = calculate_ema(closes, period=settings["EMA_LONG_PERIOD"])
    trend = detect_trend(ema_short, ema_long)
    sideways = detect_sideways(closes)
    stars = generate_stars(rsi, trend, sideways)

    return format_analysis(symbol, rsi, ema_short, ema_long, trend, stars, lang)

def calculate_rsi(prices: list, period: int = 14) -> float:
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def calculate_ema(prices: list, period: int) -> float:
    ema = sum(prices[:period]) / period
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return round(ema, 2)

def detect_trend(ema_short: float, ema_long: float) -> str:
    if ema_short > ema_long:
        return "up"
    elif ema_short < ema_long:
        return "down"
    return "neutral"

def detect_sideways(prices: list, threshold: float = 0.01) -> bool:
    min_price = min(prices[-20:])
    max_price = max(prices[-20:])
    return (max_price - min_price) / min_price < threshold

def generate_stars(rsi: float, trend: str, sideways: bool) -> int:
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
            f"EMA({settings['EMA_SHORT_PERIOD']}): {ema_short} | "
            f"EMA({settings['EMA_LONG_PERIOD']}): {ema_long}\n"
            f"Trend: {trend_text[trend]['de']}\n"
            f"Bewertung: {star_str} ({stars}/5)"
        )
    else:
        return (
            f"Analysis for {symbol}:\n"
            f"RSI: {rsi}\n"
            f"EMA({settings['EMA_SHORT_PERIOD']}): {ema_short} | "
            f"EMA({settings['EMA_LONG_PERIOD']}): {ema_long}\n"
            f"Trend: {trend_text[trend]['en']}\n"
            f"Rating: {star_str} ({stars}/5)"
        )
