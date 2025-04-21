from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application, MessageHandler, filters
import json

async def webhook_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = json.loads(update.message.text)
        symbol = data.get("symbol", "Unknown")
        action = data.get("action", "none").capitalize()
        confidence = data.get("confidence", 3)
        pattern = data.get("pattern", "Neutral")
        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        message = (
            f"🚨 *Webhook-Signal erhalten!*\n"
            f"Symbol: *{symbol}*\n"
            f"Aktion: *{action}*\n"
            f"Muster: *{pattern}*\n"
            f"Vertrauen: {stars}"
        )

        await update.message.reply_markdown(message)

    except Exception as e:
        await update.message.reply_text("❌ Fehler beim Verarbeiten des Webhooks.")
        print(f"Webhook Error: {e}")

webhook_handler_command = MessageHandler(filters.TEXT & ~filters.COMMAND, webhook_handler)