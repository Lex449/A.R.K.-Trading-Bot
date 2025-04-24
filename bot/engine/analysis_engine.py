# bot/engine/analysis_engine.py

from bot.engine.data_provider import get_candles
from bot.utils.indicator import calculate_rsi, calculate_ema, detect_candlestick_pattern
from bot.config.settings import get_settings

settings = get_settings()

def analyze_market(symbol: str):
    candles = get_candles(symbol)
    if not candles or len(candles) < 50:
        return None

    closes = candles["close"].tolist()

    rsi_values = calculate_rsi(closes, settings["RSI_PERIOD"])
    ema_short = calculate_ema(closes, settings["EMA_SHORT_PERIOD"])
    ema_long = calculate_ema(closes, settings["EMA_LONG_PERIOD"])

    if not rsi_values or not ema_short or not ema_long:
        return None

    rsi = rsi_values[-1]
    pattern = detect_candlestick_pattern(candles)
    trend = "Uptrend" if ema_short[-1] > ema_long[-1] else "Downtrend"

    # Signal-Entscheidung
    signal = None
    if rsi < 30 and pattern in ["Hammer", "Bullish Engulfing"]:
        signal = "LONG"
    elif rsi > 70 and pattern in ["Shooting Star", "Bearish Engulfing"]:
        signal = "SHORT"

    confidence = 1
    if signal == "LONG" and rsi < 25:
        confidence = 5
    elif signal == "SHORT" and rsi > 75:
        confidence = 5
    elif signal:
        confidence = 3

    return {
        "symbol": symbol,
        "price": candles["close"].iloc[-1],
        "rsi": round(rsi, 2),
        "trend": trend,
        "pattern": pattern,
        "signal": signal,
        "confidence": confidence
    }
