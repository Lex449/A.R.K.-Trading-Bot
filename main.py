"""
A.R.K. – Main Launcher.
Single event-loop, nest_asyncio-Fallback für Railway.
Made in Bali. Engineered with German Precision.
"""

import asyncio
from telegram.ext import ApplicationBuilder
from bot.config.settings import get_settings
from bot.startup.startup_task import startup_task
from bot.utils.logger import setup_logger

logger   = setup_logger(__name__)
settings = get_settings()


async def _run_bot() -> None:
    """Baut Application, führt Startup-Tasks aus, startet Long-Polling."""
    application = (
        ApplicationBuilder()
        .token(settings["BOT_TOKEN"])
        .build()
    )

    # Scheduler / Heartbeat / Jobs initialisieren
    await startup_task(application)

    # Blockiert bis SIGTERM
    await application.run_polling(poll_interval=1.0)


def main() -> None:
    """Garantiert genau eine asyncio-Event-Loop, auch auf Railway."""
    try:
        asyncio.run(_run_bot())
    except RuntimeError as exc:
        # Railway startet Python oft in bereits laufender Loop
        if "running event loop" in str(exc):
            import nest_asyncio  # type: ignore
            nest_asyncio.apply()
            logger.warning("⚠️  Running loop patched via nest_asyncio.")
            asyncio.run(_run_bot())
        else:
            raise


if __name__ == "__main__":
    main()
