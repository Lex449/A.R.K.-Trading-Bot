import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.config.settings import get_settings
from bot.utils.error_handler import handle_error

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("BOT_TOKEN fehlt!")

app = ApplicationBuilder().token(bot_token).build()

app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(signal_handler)
app.add_handler(status_handler)

app.add_error_handler(handle_error)

if __name__ == "__main__":
    app.run_polling()