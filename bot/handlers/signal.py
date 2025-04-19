from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.language import get_language

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    try:
        data = analyse_market()

        trend = data["trend"]
        confidence = data["confidence"]
        pattern = data.get("pattern", "Unbekannt")
        timestamp = data["timestamp"]

        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        messages = {
            "de": (
                f"📈 *Marktsignal erkannt!*\n\n"
                f"• Trend: *{trend}*\n"
                f"• Muster: *{pattern}*\n"
                f"• Vertrauen: {stars}\n"
                f"• Zeit: `{timestamp}`\n\n"
                f"_Automatische Analyse abgeschlossen._"
            ),
            "en": (
                f"📈 *Market signal detected!*\n\n"
                f"• Trend: *{trend}*\n"
                f"• Pattern: *{pattern}*\n"
                f"• Confidence: {stars}\n"
                f"• Time: `{timestamp}`\n\n"
                f"_Automatic analysis complete._"
            )
        }

        await update.message.reply_text(messages[lang], parse_mode="Markdown")

    except Exception as e:
        fallback = {
            "de": "⚠️ Fehler beim Analysieren des Marktes.",
            "en": "⚠️ Error during market analysis."
        }
        await update.message.reply_text(fallback[lang])
        print(f"[ERROR in /signal]: {e}")

signal_handler = CommandHandler("signal", signal)