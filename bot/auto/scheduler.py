# bot/auto/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_analysis import daily_analysis_job

def setup_scheduler(application):
    scheduler = AsyncIOScheduler()

    # Tägliche Analyse einmal pro Tag um 16:00 Bali-Zeit
    scheduler.add_job(
        daily_analysis_job,
        trigger="cron",
        hour=16,
        minute=0,
        timezone="Asia/Makassar",  # WITA (Bali)
        args=[application]
    )

    # AutoSignal Loop (läuft ohnehin dauerhaft)
    application.create_task(auto_signal_loop())

    scheduler.start()
