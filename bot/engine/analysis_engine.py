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

async def analyze_market(symbol: str):
    """Analysiert das Symbol und gibt das Signal zurück."""
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

    return {
        "price": closes[-1],  # Letzter Preis
        "signal": "BUY" if trend == "up" else "SELL",  # Signal basierend auf dem Trend
        "rsi": rsi,
        "trend": trend,
        "pattern": "bullish" if trend == "up" else "bearish",  # Muster, basierend auf dem Trend
        "stars": stars
    }

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
