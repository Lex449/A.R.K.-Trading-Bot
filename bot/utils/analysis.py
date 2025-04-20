import pandas as pd
import ta

def analyse_market(symbol: str):
    data = pd.DataFrame({
        'close': [100, 102, 101, 105, 107, 110, 108],
    })
    data['rsi'] = ta.momentum.RSIIndicator(data['close']).rsi()
    data['ema'] = ta.trend.EMAIndicator(data['close']).ema_indicator()

    last = data.iloc[-1]
    trend = "Long" if last['close'] > last['ema'] else "Short"
    pattern = "Neutral"
    confidence = 4 if 30 < last['rsi'] < 70 else 2

    return {"trend": trend, "pattern": pattern, "confidence": confidence}