"""
A.R.K. Startup Engine – Ultimate Bot Launcher.
Handles all critical boot tasks safely, sequentially, fault-tolerant.
"""

import asyncio
import logging
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.heartbeat_scheduler import start_heartbeat
from bot.auto.watchdog_scheduler import start_watchdog  # NEU
from bot.handlers.set_my_commands import set_bot_commands
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup logger
logger = logging.getLogger(__name__)
config = get_settings()

async def startup_tasks(application):
    """
    Executes all essential startup tasks safely.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        # === Remove Webhook for clean polling ===
        await application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook removed successfully.")

        # === Set Bot Command List ===
        await set_bot_commands(application)
        logger.info("✅ Bot commands set successfully.")

        # === Start Schedulers ===
        start_daily_analysis_scheduler(application, chat_id)
        logger.info("✅ Daily Analysis Scheduler started.")

        start_heartbeat(application, chat_id)
        logger.info("✅ Heartbeat Scheduler started.")

        # Optional: Start Watchdog if enabled
        if config.get("WATCHDOG_ENABLED", True):
            start_watchdog(application, chat_id)
            logger.info("✅ Watchdog Scheduler started.")

        # === Start Auto-Signal Loop ===
        from bot.auto.auto_signal_loop import auto_signal_loop
        asyncio.create_task(auto_signal_loop())
        logger.info("✅ Auto-Signal Loop launched successfully.")

        logger.info("🚀 All Startup Tasks completed. Bot is now fully operational.")

    except Exception as e:
        logger.error(f"❌ Startup Tasks Error: {e}")
        await report_error(application.bot, chat_id, e, context_info="Startup Phase")
