from telegram.ext import ApplicationBuilder
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.config.settings import get_settings

settings = get_settings()
app = ApplicationBuilder().token(settings["telegram"]["token"]).build()

# Handler hinzufügen
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)

if __name__ == '__main__':
    print("A.R.K. läuft im Mentor-Modus...")
    app.run_polling()