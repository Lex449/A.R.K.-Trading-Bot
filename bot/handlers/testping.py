from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def testping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Test-Ping erfolgreich. A.R.K. antwortet.")

testping_handler = CommandHandler("testping", testping)