"""
Heartbeat Job – hält den Bot am Leben, liefert System-Metriken
und verhindert Doppel-Instanzen durch einen Redis-Lock (optional).

Made in Bali. Engineered with German Precision.
"""

import asyncio
import datetime as _dt
import platform
import psutil
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

logger = setup_logger(__name__)
settings = get_settings()

# ──────────────────────────────────────────────────────────────
# OPTIONAL: Doppel-Instanz-Schutz via Redis-Lock
# Wenn du keinen Redis hast, lass LOCK = None
# ──────────────────────────────────────────────────────────────
LOCK = None
try:
    import aioredis

    async def _redis_lock():
        redis = await aioredis.from_url(settings.get("REDIS_URL", "redis://localhost"))
        locked = await redis.setnx("ark:heartbeat_lock", "1")
        if locked:
            await redis.expire("ark:heartbeat_lock", 3600)
        return locked

    LOCK = _redis_lock
except ImportError:
    pass


async def heartbeat_job(bot: Bot, chat_id: int) -> None:
    """Sendet alle 60 Minuten einen Heartbeat + System-Metriken."""
    if LOCK and not await LOCK():
        logger.warning("⏩ Heartbeat übersprungen – Lock verhindert Doppel-Ping.")
        return

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    now = _dt.datetime.utcnow().strftime("%H:%M UTC")

    text = (
        "🫀 <b>Heartbeat</b>\n"
        f"• Host <i>{platform.node()}</i>\n"
        f"• CPU {cpu:.1f}%  RAM {ram:.1f}%\n"
        f"• Time {now}"
    )

    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        logger.info("✅ Heartbeat gesendet.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("❌ Heartbeat fehlgeschlagen: %s", exc)
        # optional: Retry nach 30 s
        await asyncio.sleep(30)
        try:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
            logger.info("✅ Heartbeat Retry erfolgreich.")
        except Exception:
            logger.exception("🔥 Heartbeat Retry endgültig gescheitert.")
