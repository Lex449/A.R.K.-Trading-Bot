import random
from telegram import Update
from telegram.ext import ContextTypes

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code
    direction = random.choice(["Long", "Short"])
    stars = random.randint(2, 5)
    emoji = "📈" if direction == "Long" else "📉"
    star_str = "★" * stars + "☆" * (5 - stars)

    if lang == "de":
        text = (
            f"{emoji} *ARK-Einstiegssignal*\n\n"
            f"Richtung: *{direction}*\n"
            f"Stärke: {star_str}\n"
            f"Dies ist eine schnelle Einschätzung. Bitte analysiere den Markt, bevor du einsteigst."
        )
    else:
        text = (
            f"{emoji} *ARK Entry Signal*\n\n"
            f"Direction: *{direction}*\n"
            f"Strength: {star_str}\n"
            f"This is a quick estimate. Always analyze the market before entering."
        )

    await update.message.reply_markdown(text)