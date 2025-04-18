from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings

settings = get_settings()

def detect_language(text: str) -> str:
    if any(word in text.lower() for word in ["hello", "hi", "/start"]):
        return "en"
    elif any(word in text.lower() for word in ["hallo", "hey", "/start"]):
        return "de"
    return "en"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    lang = detect_language(update.message.text)

    if user_id != settings["DANIEL_TELEGRAM_ID"]:
        await update.message.reply_text("Access denied.")
        return

    if lang == "de":
        text = (
            "*Willkommen bei A.R.K.*, deinem Trading-Mentor.\n\n"
            "Bereit zum Durchstarten? Hier sind deine Befehle:\n"
            "• `/ping` – Verbindung testen\n"
            "• `/status` – Systemstatus\n"
            "• `/signal` – Marktsignal erhalten\n"
            "• `/analyse` – Marktanalyse starten\n"
            "• `/shutdown` – Bot stoppen\n\n"
            "_Lass uns gemeinsam klüger traden. Los geht’s!_ 🚀"
        )
    else:
        text = (
            "*Welcome to A.R.K.*, your personal trading mentor.\n\n"
            "Ready to launch? Use these commands:\n"
            "• `/ping` – Test connection\n"
            "• `/status` – Check system status\n"
            "• `/signal` – Get market signal\n"
            "• `/analyse` – Start market analysis\n"
            "• `/shutdown` – Stop the bot\n\n"
            "_Let’s trade smarter, together. Let’s go!_ 🚀"
        )

    await update.message.reply_text(text, parse_mode="Markdown")

start_handler = CommandHandler("start", start_command)