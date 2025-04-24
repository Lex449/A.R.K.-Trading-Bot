from bot.data_provider import get_historical_data
from bot.indicators import compute_ema, compute_rsi

def check_signal(symbol: str):
    df = get_historical_data(symbol)
    if df is None or len(df) < max(RSI_PERIOD, EMA_LONG_PERIOD): 
        return None
    close = df["close"]

    ema_s = compute_ema(close, EMA_SHORT_PERIOD)
    ema_l = compute_ema(close, EMA_LONG_PERIOD)
    rsi = compute_rsi(close, RSI_PERIOD)

    last_ema_s = ema_s.iloc[-1]
    last_ema_l = ema_l.iloc[-1]
    last_rsi = rsi.iloc[-1]

    # Beispiel-Regeln: EMA-Crossover + RSI-Schwellen
    if last_ema_s > last_ema_l and last_rsi < 30:
        return "BUY"
    if last_ema_s < last_ema_l and last_rsi > 70:
        return "SELL"
    return None
