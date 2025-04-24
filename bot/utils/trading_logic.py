# bot/utils/trading_logic.py

from bot.utils.data_provider import get_market_data
from bot.utils.indicators import analyze_candles


def generate_trade_signal(symbol: str, interval: str = "5min") -> dict:
    """
    Holt Marktdaten, analysiert den Chart und generiert ein Handelssignal.
    """

    df = get_market_data(symbol, interval)

    if df is None or df.empty:
        return {
            "symbol": symbol,
            "signal": None,
            "comment": "❌ Keine Daten gefunden"
        }

    analysis = analyze_candles(df)

    return {
        "symbol": symbol,
        "price": df['close'].iloc[-1],
        "rsi": analysis["rsi"],
        "ema_short": analysis["ema_short"],
        "ema_long": analysis["ema_long"],
        "pattern": analysis["pattern"],
        "trend": analysis["trend"],
        "signal": analysis["signal"],
        "confidence": analysis["confidence"],
        "comment": analysis["comment"]
    }
