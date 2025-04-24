# bot/engine/analysis.py

from bot.engine.data_provider import fetch_data
from bot.engine.trading_logic import analyze_trend

def run_analysis(symbols: list):
    summary = []
    ranking = []
    strong_setups = []

    for symbol in symbols:
        result = analyze_trend(symbol)
        if not result:
            continue

        signal = result["signal"]
        trend = result["trend"]
        rsi = round(result["rsi"], 2)
        pattern = result["pattern"]
        price = result["price"]
        confidence = result["confidence"]
        comment = result["comment"]
        emoji = result["emoji"]

        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        # Ranking
        ranking.append(f"`TOP` *{symbol}* {emoji} {stars}")

        # Nur starke Signale anzeigen
        if confidence >= 3:
            block = (
                f"*{symbol}* {emoji}\n"
                f"> *Signal:* `{signal}`\n"
                f"> *Preis:* `{price}` | *Trend:* {trend}\n"
                f"> *RSI:* `{rsi}` | *Muster:* {pattern}\n"
                f"> *Qualität:* {stars}\n"
                f"_→ {comment}_\n"
            )
            strong_setups.append(block)

    # Sortiere nach Confidence
    ranking = sorted(ranking, reverse=True)

    return summary, ranking, strong_setups
