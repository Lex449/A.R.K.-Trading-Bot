from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code

    if lang == "de":
        message = (
            "🛠️ *Hilfe & Übersicht*\n\n"
            "Ich bin A.R.K., dein KI-Trading-Mentor.\n"
            "Hier sind meine wichtigsten Befehle:\n\n"
            "`/start` – Begrüßung & Einstieg\n"
            "`/analyse` – Marktscan + Einstiegssignale\n"
            "`/status` – Systemstatus & Bot-Zustand\n"
            "`/signal` – Direktes Signal anfordern\n"
            "`/shutdown` – Bot stoppen (Admin)\n\n"
            "💬 Fragen oder Austausch? 👉 [Community beitreten](https://t.me/arktradingcommunity)"
        )
    else:
        message = (
            "🛠️ *Help & Overview*\n\n"
            "I'm A.R.K., your AI trading mentor.\n"
            "Here are my most useful commands:\n\n"
            "`/start` – Introduction & welcome\n"
            "`/analyse` – Market scan + trade signals\n"
            "`/status` – System status & bot health\n"
            "`/signal` – Get a direct entry signal\n"
            "`/shutdown` – Stop the bot (admin)\n\n"
            "💬 Questions or support? 👉 [Join the community](https://t.me/arktradingcommunity)"
        )

    await update.message.reply_markdown(message, disable_web_page_preview=True)