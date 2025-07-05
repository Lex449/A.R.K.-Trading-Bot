"""
Connection-Watchdog: prüft Bot-Erreichbarkeit & Telegram-API-Ping.
"""

import httpx
from telegram import Bot
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)


async def check_connection(bot: Bot, chat_id: int) -> None:
    """Sendet Ping, wenn Telegram API down oder Bot getrennt."""
    try:
        # Mini-Ping: getMe
        await bot.get_me()

        # Extra: prüfe Telegram Status-Endpoint
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get("https://api.telegram.org")
            if r.status_code != 200:
                raise RuntimeError("Telegram API unreachable")

    except Exception as exc:
        logger.error("❌ [Watchdog] Connection lost: %s", exc)
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=f"⚠️ <b>Watchdog-Alarm</b>\n<code>{exc}</code>",
                parse_mode="HTML",
            )
        except Exception:
            logger.exception("🔥 [Watchdog] Failed to send alarm.")
