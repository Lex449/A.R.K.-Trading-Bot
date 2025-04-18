from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await analyse_market()

    if result is None:
        await update.message.reply_text("⚠️ Kein klares Signal gefunden. Warte auf eine stärkere Bewegung...")
        return

    direction = result["direction"]
    confidence = result["confidence"]
    pattern = result.get("pattern", "Kein Muster")
    stars = "⭐" * confidence + "✩" * (5 - confidence)

    msg = (
        f"📈 *Neues Signal entdeckt!*\n"
        f"------------------------------\n"
        f"📊 *Richtung:* `{direction.upper()}`\n"
        f"🕵️ *Muster:* `{pattern}`\n"
        f"⭐ *Qualität:* {stars}\n"
        f"------------------------------\n"
        f"_Mentor-Tipp:_ Nur einsteigen, wenn du bereit bist. Keine Aktion ist auch eine Entscheidung."
    )

    await update.message.reply_markdown(msg)