from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Trader"
    lang = get_language(update)

    if lang == "de":
        msg = (
            f"👋 *Willkommen bei A.R.K.*, {name}!\n\n"
            f"Ich bin dein persönlicher KI-Trading-Mentor – spezialisiert auf schnelle, klare Signale für Index-Trading mit hoher Präzision.\n\n"
            f"✅ *Bereit für deine ersten Live-Signale?*\n"
            f"Nutze /analyse oder /signal, um sofort einzusteigen.\n\n"
            f"🔒 *100% privat. 100% skalierbar. 100% A.R.K.*\n"
            f"📣 *Tipp:* Tritt unserer Community bei: [Telegram Gruppe](https://t.me/arktradingcommunity)"
        )
    else:
        msg = (
            f"👋 *Welcome to A.R.K.*, {name}!\n\n"
            f"I'm your personal AI trading mentor – built for fast, precise index trading signals with serious power.\n\n"
            f"✅ *Ready to get your first live signals?*\n"
            f"Try /analyse or /signal to begin right now.\n\n"
            f"🔒 *100% private. 100% scalable. 100% A.R.K.*\n"
            f"📣 *Pro tip:* Join our community: [Telegram Group](https://t.me/arktradingcommunity)"
        )

    await update.message.reply_markdown(msg, disable_web_page_preview=True)

start_handler = CommandHandler("start", start)
