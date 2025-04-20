from telegram import Update
from telegram.ext import ContextTypes

# Lege dein persönliches Admin-Passwort hier fest
ADMIN_PASS = "arkshutdown123"

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code
    user_input = " ".join(context.args) if context.args else ""

    if user_input != ADMIN_PASS:
        if lang == "de":
            await update.message.reply_text("❌ Zugriff verweigert. Falsches Passwort.")
        else:
            await update.message.reply_text("❌ Access denied. Incorrect password.")
        return

    if lang == "de":
        await update.message.reply_text("🛑 Bot wird jetzt gestoppt.")
    else:
        await update.message.reply_text("🛑 Shutting down now.")

    await context.bot.shutdown()