from telegram.ext import ApplicationBuilder
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.testping import testping_handler  # NEU
from bot.config.settings import get_settings
from bot.utils.error_handler import handle_error
from bot.utils.dns_monitor import check_dns_and_notify  # NEU
import asyncio  # NEU

settings = get_settings()
app = ApplicationBuilder().token(settings["TOKEN"]).build()

app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(testping_handler)  # NEU

app.add_error_handler(handle_error)

# NEU: DNS-Monitoring beim Start aktivieren
async def run():
    await asyncio.gather(
        app.run_polling(),
        check_dns_and_notify()
    )

if __name__ == "__main__":
    asyncio.run(run())