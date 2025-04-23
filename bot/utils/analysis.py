# bot/utils/analysis.py
# Modul für Datenabruf von TwelveData und technische Analyse (RSI, EMA, Candlestick-Muster)

import requests
from bot.config import config

def fetch_time_series(symbol: str, interval: str, outputsize: int = 60):
    """Ruft OHLC-Daten für das gegebene Symbol und Intervall von TwelveData ab."""
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": config.TWELVEDATA_API_KEY
    }
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        print(f"[FEHLER] Datenabfrage für {symbol} fehlgeschlagen: {e}")
        return None
    if data.get("status") and data["status"] != "ok":
        print(f"[FEHLER] API-Fehler für {symbol}: {data.get('message')}")
        return None
    values = data.get("values")
    if not values:
        print(f"[FEHLER] Keine Daten erhalten für Symbol {symbol}")
        return None
    quotes = []
    for entry in values:
        try:
            quotes.append({
                "datetime": entry["datetime"],
                "open": float(entry["open"]),
                "high": float(entry["high"]),
                "low": float(entry["low"]),
                "close": float(entry["close"])
            })
        except KeyError:
            continue
    quotes.sort(key=lambda x: x["datetime"])
    return quotes

def calculate_rsi(closes, period: int = 14):
    if len(closes) < period + 1:
        return []
    rsi_values = []
    gains = 0.0
    losses = 0.0
    for i in range(1, period + 1):
        change = closes[i] - closes[i - 1]
        if change >= 0:
            gains += change
        else:
            losses += -change
    avg_gain = gains / period
    avg_loss = losses / period
    if avg_loss == 0:
        rsi_values.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100.0 - (100.0 / (1.0 + rs)))
    for i in range(period + 1, len(closes)):
        change = closes[i] - closes[i - 1]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))
        rsi_values.append(rsi)
    return rsi_values

def calculate_ema(closes, period: int):
    if len(closes) == 0:
        return []
    ema_values = []
    ema = closes[0]
    alpha = 2 / (period + 1)
    ema_values.append(ema)
    for price in closes[1:]:
        ema = alpha * price + (1 - alpha) * ema
        ema_values.append(ema)
    return ema_values

def detect_candlestick_pattern(quotes):
    pattern = None
    if len(quotes) >= 2:
        prev = quotes[-2]
        last = quotes[-1]
        prev_body = prev["close"] - prev["open"]
        last_body = last["close"] - last["open"]
        if prev_body < 0 and last_body > 0 and last["close"] > prev["open"] and last["open"] < prev["close"]:
            pattern = "bullish_engulfing"
        if prev_body > 0 and last_body < 0 and last["close"] < prev["open"] and last["open"] > prev["close"]:
            pattern = "bearish_engulfing"
    if len(quotes) >= 1:
        last = quotes[-1]
        body = abs(last["close"] - last["open"])
        high = last["high"]
        low = last["low"]
        upper_shadow = high - max(last["close"], last["open"])
        lower_shadow = min(last["close"], last["open"]) - low
        if body < (high - low) * 0.3 and lower_shadow > body * 2 and upper_shadow < body * 0.5 and last["close"] > last["open"]:
            pattern = "hammer"
        if body < (high - low) * 0.3 and upper_shadow > body * 2 and lower_shadow < body * 0.5 and last["close"] < last["open"]:
            pattern = "shooting_star"
    return pattern

def analyze_symbol(symbol_name: str):
    ticker = config.SYMBOLS.get(symbol_name, symbol_name)
    data = fetch_time_series(ticker, config.INTERVAL, outputsize=100)
    if data is None:
        return None
    closes = [candle["close"] for candle in data]
    rsi_series = calculate_rsi(closes, config.RSI_PERIOD)
    ema_short_series = calculate_ema(closes, config.EMA_SHORT_PERIOD)
    ema_long_series = calculate_ema(closes, config.EMA_LONG_PERIOD)
    if len(rsi_series) == 0:
        return None
    rsi_current = rsi_series[-1]
    rsi_prev = rsi_series[-2] if len(rsi_series) >= 2 else rsi_current
    ema_short_cur = ema_short_series[-1] if len(ema_short_series) > 0 else None
    ema_short_prev = ema_short_series[-2] if len(ema_short_series) > 1 else None
    ema_long_cur = ema_long_series[-1] if len(ema_long_series) > 0 else None
    ema_long_prev = ema_long_series[-2] if len(ema_long_series) > 1 else None
    pattern_code = detect_candlestick_pattern(data)
    if pattern_code == "bullish_engulfing":
        pattern_desc = "Bullish Engulfing (bullisches Umkehrmuster)"
    elif pattern_code == "bearish_engulfing":
        pattern_desc = "Bearish Engulfing (bärisches Umkehrmuster)"
    elif pattern_code == "hammer":
        pattern_desc = "Hammer (bullisch)"
    elif pattern_code == "shooting_star":
        pattern_desc = "Shooting Star (bärisch)"
    else:
        pattern_desc = "Kein besonderes Muster"
    trend = None
    if ema_short_cur is not None and ema_long_cur is not None:
        trend = "Aufwärtstrend" if ema_short_cur > ema_long_cur else "Abwärtstrend"
    signal = None
    bullish_pattern = pattern_code in ("bullish_engulfing", "hammer")
    bearish_pattern = pattern_code in ("bearish_engulfing", "shooting_star")
    golden_cross = False
    death_cross = False
    if ema_short_cur is not None and ema_long_cur is not None and ema_short_prev is not None and ema_long_prev is not None:
        golden_cross = ema_short_prev <= ema_long_prev and ema_short_cur > ema_long_cur
        death_cross = ema_short_prev >= ema_long_prev and ema_short_cur < ema_long_cur
    if rsi_current < 30 and bullish_pattern:
        signal = "LONG"
    elif rsi_current > 70 and bearish_pattern:
        signal = "SHORT"
    elif golden_cross:
        signal = "LONG"
    elif death_cross:
        signal = "SHORT"
    result = {
        "symbol": symbol_name,
        "price": data[-1]["close"],
        "rsi": rsi_current,
        "ema_short": ema_short_cur,
        "ema_long": ema_long_cur,
        "pattern": pattern_desc,
        "trend": trend,
        "signal": signal
    }
    return result
