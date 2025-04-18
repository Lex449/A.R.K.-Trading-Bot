from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.analysis import analyse_market

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Ich analysiere den Markt in Echtzeit... bitte einen Moment Geduld.")

    result = await analyse_market()

    if result is None:
        await update.message.reply_text("⚠️ Kein klares Setup gefunden. Geduld ist auch eine Position.")
        return

    direction = result["direction"]
    confidence = result["confidence"]
    pattern = result.get("pattern", "Unbekannt")
    stars = "⭐" * confidence + "✩" * (5 - confidence)

    msg = (
        f"📊 *Analyse abgeschlossen!*\n"
        f"------------------------------\n"
        f"📈 *Trendrichtung:* `{direction.upper()}`\n"
        f"🕵️ *Erkanntes Muster:* `{pattern}`\n"
        f"⭐ *Signalqualität:* {stars}\n"
        f"------------------------------\n"
        f"_Bleib fokussiert, Daniel. Timing schlägt alles._"
    )

    await update.message.reply_markdown(msg)