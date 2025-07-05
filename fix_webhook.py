import asyncio
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()

async def fix_webhook():
    """Deletes any existing Telegram webhook and drops pending updates."""
    bot = Bot(token=settings["BOT_TOKEN"])
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Webhook successfully removed.")

if __name__ == "__main__":
    asyncio.run(fix_webhook())
