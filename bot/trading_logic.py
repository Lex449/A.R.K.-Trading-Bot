# bot/trading_logic.py

from bot.engine.data_provider import get_candles
from bot.engine.indicators import compute_ema, compute_rsi
from bot.config.settings import get_settings

settings = get_settings()
RSI_PERIOD = settings["RSI_PERIOD"]
EMA_SHORT_PERIOD = settings["EMA_SHORT_PERIOD"]
EMA_LONG_PERIOD = settings["EMA_LONG_PERIOD"]

def check_signal(symbol: str):
    candles = get_candles(symbol, interval="1", limit=max(RSI_PERIOD, EMA_LONG_PERIOD) + 1)
    if not candles or len(candles) < max(RSI_PERIOD, EMA_LONG_PERIOD):
        print(f"[WARN] Nicht genug Daten für {symbol}")
        return None

    close_prices = [candle["close"] for candle in candles]

    ema_short = compute_ema(close_prices, EMA_SHORT_PERIOD)
    ema_long = compute_ema(close_prices, EMA_LONG_PERIOD)
    rsi = compute_rsi(close_prices, RSI_PERIOD)

    if not ema_short or not ema_long or not rsi:
        print(f"[WARN] Indikatorberechnung fehlgeschlagen für {symbol}")
        return None

    last_ema_short = ema_short[-1]
    last_ema_long = ema_long[-1]
    last_rsi = rsi[-1]

    # Klare Logik für Entry-Signale
    if last_ema_short > last_ema_long and last_rsi < 30:
        return "BUY"
    elif last_ema_short < last_ema_long and last_rsi > 70:
        return "SELL"
    else:
        return None
