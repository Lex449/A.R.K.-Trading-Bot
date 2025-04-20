from telegram import Update
from telegram.ext import ContextTypes

# Simulierter Recap-Speicher (später durch echte Analyse-Logs ersetzen)
RECAP_DATA = {
    "US100": {"trend": "Long", "strength": 4},
    "DAX": {"trend": "Neutral", "strength": 3},
    "Bitcoin": {"trend": "Short", "strength": 5},
    "Dow Jones": {"trend": "Long", "strength": 3}
}

def format_recap(lang: str):
    emoji_map = {
        "Long": "📈",
        "Short": "📉",
        "Neutral": "⚖️"
    }

    lines = []
    for market, data in RECAP_DATA.items():
        trend = data["trend"]
        stars = "★" * data["strength"] + "☆" * (5 - data["strength"])
        emoji = emoji_map.get(trend, "❓")

        if lang == "de":
            lines.append(f"• {market}: {emoji} {trend} {stars}")
        else:
            lines.append(f"• {market}: {emoji} {trend} {stars}")

    if lang == "de":
        return (
            "📊 *Tagesrückblick*\n\n" +
            "\n".join(lines) +
            "\n\n💡 Heute war kein perfekter Einstieg dabei? Denk dran: Manchmal ist *abwarten* die beste Strategie."
        )
    else:
        return (
            "📊 *Daily Recap*\n\n" +
            "\n".join(lines) +
            "\n\n💡 No perfect entry today? Remember: Sometimes *waiting* is the best position."
        )

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code
    text = format_recap(lang)
    await update.message.reply_markdown(text)