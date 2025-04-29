"""
A.R.K. Heartbeat Manager – Ultra Stability Pulse System
Keeps the system alive with timed heartbeat pings and recovery fallback.
"""

import logging
import asyncio
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Logger Setup
logger = setup_logger(__name__)
config = get_settings()

async def heartbeat_loop(application):
    """
    Sends a heartbeat message every 60 minutes to confirm system health.
    """
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    bot = application.bot

    logger.info("💓 [Heartbeat] Heartbeat loop started.")

    while True:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text="✅ *Heartbeat:* Bot läuft stabil und analysiert den Markt.",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info("✅ [Heartbeat] Pulse sent successfully.")

        except Exception as e:
            logger.error(f"❌ [Heartbeat] Failed to send heartbeat: {e}")

        await asyncio.sleep(3600)  # Sleep for 1 hour (3600 seconds)

async def start_heartbeat_manager(application):
    """
    Launches the heartbeat background loop safely.
    """
    try:
        asyncio.create_task(heartbeat_loop(application))
        logger.info("✅ [Heartbeat Manager] Heartbeat system initialized.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat Manager] Failed to initialize heartbeat: {e}")
