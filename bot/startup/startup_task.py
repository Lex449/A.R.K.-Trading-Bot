"""
A.R.K. Startup Task – Mission Control Sequence
Initialisiert alle Hintergrundprozesse, Scheduler, Loops und Systemdienste.
Made in Bali. Engineered with German Precision.
"""

from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.auto_analysis_scheduler import start_auto_analysis_scheduler
from bot.auto.connection_watchdog import start_watchdog_loop
from bot.auto.heartbeat_manager import start_heartbeat_loop
from bot.utils.logger import setup_logger
import asyncio

logger = setup_logger(__name__)

async def execute_startup_tasks(application):
    try:
        logger.info("🛠️ [Startup] Initialisiere Hintergrundprozesse...")

        # 1. Auto-Analysis Scheduler starten (60s Loop, Spamfrei)
        start_auto_analysis_scheduler(application)

        # 2. Auto-Signal-Loop starten (Live-Signale, Deep Diagnostics)
        asyncio.create_task(auto_signal_loop(application))

        # 3. Verbindung überwachen (Telegram, Internet, Stability)
        asyncio.create_task(start_watchdog_loop(application))

        # 4. Heartbeat senden (24/7 Bot-Ping, Verbindungscheck)
        asyncio.create_task(start_heartbeat_loop(application))

        logger.info("✅ [Startup] Alle Hintergrundprozesse erfolgreich aktiviert.")

    except Exception as e:
        logger.exception(f"❌ [Startup] Fehler beim Initialisieren der Tasks: {e}")
