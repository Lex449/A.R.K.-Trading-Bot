"""
A.R.K. – Ultra Resilient Main Entry Point.
Made in Bali. Engineered with German Precision.
"""

from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import (
    start, help_command, analyze_symbol_handler, signal_handler,
    status_handler, uptime_handler, set_language_handler, shutdown_handler
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.startup.startup_task import execute_startup_tasks

logger = setup_logger(__name__)
config = get_settings()

async def post_init(application):
    await execute_startup_tasks(application)

def main():
    logger.info("🚀 [Main] Launch sequence initiated...")

    application = (
        ApplicationBuilder()
        .token(config["BOT_TOKEN"])
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    application.add_handler(CommandHandler("signal", signal_handler))
    application.add_handler(CommandHandler("status", status_handler))
    application.add_handler(CommandHandler("uptime", uptime_handler))
    application.add_handler(CommandHandler("setlanguage", set_language_handler))
    application.add_handler(CommandHandler("shutdown", shutdown_handler))

    application.add_error_handler(global_error_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
