from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

recap_text = (
    "🧾 *Tägliches Recap (Beta)*\n"
    "-----------------------------\n"
    "• Gewinne heute: +21 €\n"
    "• Verluste heute: -8 €\n"
    "• Qualität der Signale: ⭐️⭐️⭐️⭐️✩\n\n"
    "_Weitere Auswertungen folgen bald._"
)

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(recap_text)

recap_handler = CommandHandler("recap", recap)
