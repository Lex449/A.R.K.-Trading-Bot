# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        market_data = analyse_market()

        trend = market_data.get("trend", "unknown")
        confidence = market_data.get("confidence", 0)
        pattern = market_data.get("pattern", "N/A")
        timestamp = market_data.get("timestamp", "")

        message = (
            f"📈 *Marktsignal erkannt!*\n\n"
            f"• Trend: *{trend}*\n"
            f"• Muster: *{pattern}*\n"
            f"• Vertrauen: {'⭐️' * confidence}\n"
            f"• Zeit: `{timestamp}`\n\n"
            f"_Automatische Analyse abgeschlossen._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("Fehler beim Generieren des Signals.")
        print(f"[Fehler in /signal]: {e}")