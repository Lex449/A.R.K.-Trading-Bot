from telegram import Update
from telegram.ext import ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code

    if lang == "de":
        message = (
            "📡 *Systemstatus*\n\n"
            "✅ A.R.K. ist *online* und bereit für deine Anfragen.\n"
            "🧠 Analysemodul: *aktiviert*\n"
            "🔒 Sicherheitsfeatures: *eingeschaltet*\n"
            "🕒 Letzte Systemprüfung: *gerade eben*\n\n"
            "Brauche ich Hilfe? Nutze `/help` oder frag in der Community."
        )
    else:
        message = (
            "📡 *System Status*\n\n"
            "✅ A.R.K. is *online* and ready to assist.\n"
            "🧠 Analysis module: *active*\n"
            "🔒 Security checks: *enabled*\n"
            "🕒 Last system check: *just now*\n\n"
            "Need help? Type `/help` or ask in the community."
        )

    await update.message.reply_markdown(message)