# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }

    mood = {
        5: "Ausrufezeichen-Trade! Du weißt, was zu tun ist.",
        4: "Sehr starkes Signal – Fokus & Entry prüfen.",
        3: "Gutes Setup, aber keine Eile. Augen auf.",
        2: "Mittelmäßig. Warte lieber noch.",
        1: "Riskant! Finger weg. A.R.K. beobachtet weiter.",
    }

    emoji = emojis.get(trend, "📊")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)
    guidance = mood.get(confidence, "")

    message = (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* {trend}\n"
        f"📊 *Muster:* {pattern}\n"
        f"⭐️ *Qualität:* {stars}\n\n"
        f"🧠 _{guidance}_\n"
        f"🤖 _A.R.K. analysiert weiter... bleib fokussiert._"
    )

    return message
