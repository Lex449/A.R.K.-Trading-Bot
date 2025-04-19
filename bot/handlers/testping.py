from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def testping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ A.R.K. meldet sich live: Verbindung funktioniert, Boss!")

testping_handler = CommandHandler("testping", testping)