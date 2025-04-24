# /bot/handlers/recap.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from datetime import datetime

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sendet einen Platzhalter für den Tagesrückblick."""

    now = datetime.now().strftime("%d.%m.%Y")
    message = (
        f"📊 *A.R.K. Daily Recap – {now}*\n"
        "--------------------------------------\n"
        "Dieses Feature befindet sich aktuell in der Entwicklung.\n\n"
        "🔜 In Zukunft siehst du hier deine erfolgreichsten Signale, Marktchancen, und mehr.\n\n"
        "_Bleib gespannt. Du wirst überrascht sein, was kommt._"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

# === Handler exportieren ===
recap_handler = CommandHandler("recap", recap)
