# bot/handlers/recap.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🧾 *Tägliches Recap (Beta)*
"
        "━━━━━━━━━━━━━━━━━━━━━
"
        "✅ Überwachte Märkte: US100, US30, NAS100, SPX500
"
        "📡 Signale heute: 3 erkannt
"
        "📈 Bestes Muster: US100 (Bullish Breakout)
"
        "📉 Warnung: NAS100 (Bearish Engulfing)
"
        "━━━━━━━━━━━━━━━━━━━━━
"
        "🔎 _Dein Rückblick powered by A.R.K._"
    )
    await update.message.reply_markdown(message)

recap_handler = CommandHandler("recap", recap)
