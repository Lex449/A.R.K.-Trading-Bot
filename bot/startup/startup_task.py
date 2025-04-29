"""
A.R.K. Startup Task Engine – Ultra Precision Launch Build 2025.
Boots all critical systems safely, reliably, and fault-tolerantly.
"""

import asyncio
import logging
from bot.auto.heartbeat_manager import start_heartbeat
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.handlers.set_my_commands import set_bot_commands
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)
config = get_settings()

async def startup_tasks(application):
    """
    Sequentially and safely executes all startup processes.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        # === 1. Remove Webhook to avoid conflict with polling ===
        await application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ [Startup] Webhook removed successfully.")

        # === 2. Set Commands (e.g., /start, /help etc.) ===
        await set_bot_commands(application)
        logger.info("✅ [Startup] Bot commands set successfully.")

        # === 3. Start Heartbeat (every hour status ping) ===
        start_heartbeat(application, chat_id)
        logger.info("✅ [Startup] Heartbeat Scheduler started.")

        # === 4. Start Daily Market Scan Scheduler ===
        start_daily_analysis_scheduler(application, chat_id)
        logger.info("✅ [Startup] Daily Analysis Scheduler started.")

        # === 5. Start Auto Signal Monitoring (async) ===
        asyncio.create_task(auto_signal_loop())
        logger.info("✅ [Startup] Auto Signal Loop launched successfully.")

        logger.info("🚀 [Startup] All systems booted successfully. A.R.K. is fully operational.")

    except Exception as e:
        logger.critical(f"🔥 [Startup] Fatal error during startup: {e}")
        await report_error(application.bot, chat_id, e, context_info="Fatal Error in Startup Tasks")
