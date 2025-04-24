# bot/handlers/recap.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from datetime import datetime

recap_handler = CommandHandler("recap", lambda update, context: recap(update, context))

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    lang = update.effective_user.language_code or "en"

    date_str = datetime.now().strftime("%d.%m.%Y")

    if lang.startswith("de"):
        message = (
            f"📊 *A.R.K. Tagesrückblick ({date_str})*\n"
            f"──────────────────────────────\n"
            f"Hallo {name},\n"
            f"der heutige Handelstag ist abgeschlossen.\n\n"
            f"Was lief gut?\n"
            f"• Klar erkennbare Trends?\n"
            f"• Gute Entry-Disziplin?\n"
            f"• Emotionen im Griff?\n\n"
            f"Wenn ja – stark. Wenn nicht – besser wird man nur durch Reflexion.\n\n"
            f"_Bleib konsequent. Dein A.R.K.-Mentor ist morgen wieder da._"
        )
    else:
        message = (
            f"📊 *A.R.K. Daily Recap ({date_str})*\n"
            f"──────────────────────────────\n"
            f"Hi {name},\n"
            f"today’s session is done.\n\n"
            f"What went well?\n"
            f"• Clear trend setups?\n"
            f"• Clean entries?\n"
            f"• Emotions in check?\n\n"
            f"If yes – great. If not – learn, don’t repeat.\n\n"
            f"_Stick to the plan. Your A.R.K. mentor is back tomorrow._"
        )

    await update.message.reply_markdown(message)
