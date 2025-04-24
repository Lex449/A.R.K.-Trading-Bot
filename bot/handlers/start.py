# /bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name or "Trader"
    lang = get_language(update)

    if lang == "de":
        welcome = (
            f"Willkommen bei *A.R.K.*, {name}!\n\n"
            "Ich bin dein KI-Trading-Mentor.\n"
            "Ich analysiere für dich rund um die Uhr die Märkte und liefere präzise Einstiegssignale.\n\n"
            "⚙️ Befehle:\n"
            "`/analyse` – Live-Marktüberblick\n"
            "`/signal` – Signal für Top-Assets\n"
            "`/status` – Bot-Check\n"
            "`/recap` – Tagesrückblick\n"
            "`/shutdown` – Bot beenden (Admin only)\n\n"
            "👉 Tritt der Community bei: [A.R.K. Telegram-Gruppe](https://t.me/arktradingcommunity)"
        )
    else:
        welcome = (
            f"Welcome to *A.R.K.*, {name}!\n\n"
            "I'm your AI trading mentor.\n"
            "I scan the markets 24/7 and deliver precise entry signals.\n\n"
            "⚙️ Commands:\n"
            "`/analyse` – Live market overview\n"
            "`/signal` – Signal for top assets\n"
            "`/status` – Bot check\n"
            "`/recap` – Daily recap\n"
            "`/shutdown` – Stop bot (Admin only)\n\n"
            "👉 Join the community: [A.R.K. Telegram Group](https://t.me/arktradingcommunity)"
        )

    await update.message.reply_markdown(welcome, disable_web_page_preview=True)

# === Handler exportieren ===
start_handler = CommandHandler("start", start)
