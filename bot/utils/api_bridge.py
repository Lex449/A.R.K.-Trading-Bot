"""
A.R.K. API Bridge – Ultra Precision Monitor Layer 2.0
Zentrale Singleton-Instanz zur API-Nutzungskontrolle, Logging und Stabilitätsmessung.

Made in Bali. Engineered with German Precision.
"""

from datetime import datetime
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

class APIUsageMonitor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.call_count = 0
        self.start_time = datetime.utcnow()

    def record_call(self, source: str = None):
        self.call_count += 1
        if source:
            logger.debug(f"📡 [API Monitor] Call recorded from: {source}")
        else:
            logger.debug("📡 [API Monitor] Call recorded.")

    def get_call_count(self) -> int:
        return self.call_count

    def get_elapsed_minutes(self) -> float:
        elapsed = datetime.utcnow() - self.start_time
        return max(elapsed.total_seconds() / 60, 1e-6)

    def get_rate_per_minute(self) -> float:
        return round(self.call_count / self.get_elapsed_minutes(), 2)

    def get_average_confidence(self) -> float:
        # Placeholder for session-based learning module (optional Erweiterung)
        return 72.5

    def get_status_summary(self) -> str:
        return (
            f"📊 *API Status Summary*\n"
            f"• Total Calls: `{self.call_count}`\n"
            f"• Duration: `{self.get_elapsed_minutes():.1f} min`\n"
            f"• Call Rate: `{self.get_rate_per_minute():.2f}/min`\n"
        )

# === Singleton Export ===
monitor = APIUsageMonitor()

def record_call(source: str = None):
    """Externer Shortcut für record_call()."""
    monitor.record_call(source)
