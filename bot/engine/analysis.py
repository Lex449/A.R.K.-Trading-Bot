# bot/engine/analysis.py

from bot.engine.trading_logic import analyze_trend

def run_analysis(symbols: list):
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

        # Sterne-Bewertung für das Ranking
        stars = "⭐️" * confidence + "✩" * (5 - confidence)
        ranking.append(f"`TOP` *{symbol}* {emoji} {stars}")

        # Nur starke Setups ab Confidence 3 anzeigen
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

    # Sortiere das Ranking nach Anzahl Sterne (Confidence)
    ranking = sorted(ranking, reverse=True)

    return ranking, strong_setups
