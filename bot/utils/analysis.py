import requests

def generate_signal(market, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={market}&interval=15min&outputsize=50&apikey={api_key}"
    response = requests.get(url).json()

    try:
        candles = response['values']
        close_prices = [float(c['close']) for c in candles]
        rsi = calculate_rsi(close_prices)
        ema = calculate_ema(close_prices)

        last_candle = candles[0]
        pattern = detect_candlestick(last_candle)

        signal = "Long" if rsi < 30 else "Short" if rsi > 70 else "Neutral"
        rating = rate_signal(signal, rsi, pattern)

        return {
            "signal": signal,
            "rsi": rsi,
            "ema": ema,
            "pattern": pattern,
            "rating": rating
        }
    except:
        return None

def calculate_rsi(prices, period=14):
    deltas = [prices[i] - prices[i+1] for i in range(len(prices)-1)]
    gains = sum([d for d in deltas[:period] if d > 0])
    losses = abs(sum([d for d in deltas[:period] if d < 0]))
    rs = gains / losses if losses != 0 else 1
    return 100 - (100 / (1 + rs))

def calculate_ema(prices, period=14):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:period]:
        ema = price * k + ema * (1 - k)
    return ema

def detect_candlestick(candle):
    o = float(candle['open'])
    h = float(candle['high'])
    l = float(candle['low'])
    c = float(candle['close'])

    if c > o and (c - o) > (h - l) * 0.5:
        return "Bullish Engulfing"
    elif o > c and (o - c) > (h - l) * 0.5:
        return "Bearish Engulfing"
    else:
        return "Neutral"

def rate_signal(signal, rsi, pattern):
    score = 3
    if signal in ["Long", "Short"]:
        score += 1
    if pattern != "Neutral":
        score += 1
    if rsi < 20 or rsi > 80:
        score += 1
    return min(score, 5)