from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.config.settings import get_settings

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = user.language_code or "en"

    if lang.startswith("de"):
        message = (
            f"Willkommen bei *A.R.K.*, {user.first_name}!\n\n"
            "Ich bin dein persönlicher KI-Trading-Mentor.\n"
            "Ich unterstütze dich dabei, die Märkte zu verstehen, Fehler zu vermeiden und sicher Vermögen aufzubauen.\n\n"
            "⚙️ Die Systeme sind aktiv.\n"
            "📡 Die Marktüberwachung läuft bereits im Hintergrund.\n\n"
            "📬 *Community-Beitritt*: [Telegram-Gruppe öffnen](https://t.me/arktradingcommunity)"
        )
    else:
        message = (
            f"Welcome to *A.R.K.*, {user.first_name}!\n\n"
            "I'm your personal AI trading mentor.\n"
            "I’ll help you understand the markets, avoid mistakes, and build wealth with confidence.\n\n"
            "⚙️ All systems are operational.\n"
            "📡 Market monitoring is already running in the background.\n\n"
            "📬 *Join the community*: [Join Telegram Group](https://t.me/arktradingcommunity)"
        )

    await update.message.reply_markdown(message, disable_web_page_preview=True)

start_handler = CommandHandler("start", start)