# bot/analytics/win_loss_report.py

"""
Generates win/loss reports for daily/weekly trading session review.
"""

from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary

def generate_win_loss_report():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    performance = get_performance_summary()

    return (
        f"📊 *Win/Loss Report*\n"
        f"Generated: {now}\n\n"
        f"{performance}\n"
        f"🧠 _Stay focused and disciplined._"
    )
