from telegram import Update
from telegram.ext import ContextTypes

# Funktion, die vom Bot beim /start-Befehl aufgerufen wird
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Willkommen bei A.R.K. – deinem persönlichen Trading-Mentor.\n"
        "Schreib /ping, um einen Verbindungstest zu machen,\n"
        "oder /signal, um dein erstes Einstiegssignal zu erhalten!"
    )