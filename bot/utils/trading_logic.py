from bot.engine.data_provider import get_candles
from bot.utils.indicators import analyze_candles


def generate_trade_signal(symbol: str, interval: str = "1") -> dict:
    """
    Holt Marktdaten im gewünschten Intervall, analysiert den Chart
    und generiert ein strukturiertes Handelssignal auf Basis von RSI, EMA und Patterns.
    """

    candles = get_candles(symbol=symbol, interval=interval)

    if not candles:
        return {
            "symbol": symbol,
            "signal": None,
            "comment": "❌ Keine Marktdaten verfügbar"
        }

    analysis = analyze_candles(candles)

    return {
        "symbol": symbol,
        "price": candles[-1]["close"],
        "rsi": analysis["rsi"],
        "ema_short": analysis["ema_short"],
        "ema_long": analysis["ema_long"],
        "pattern": analysis["pattern"],
        "trend": analysis["trend"],
        "signal": analysis["signal"],
        "confidence": analysis["confidence"],
        "comment": analysis["comment"]
    }
