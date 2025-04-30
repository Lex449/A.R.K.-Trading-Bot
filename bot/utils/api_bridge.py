"""
A.R.K. API Bridge – Safe Singleton Export Layer
Verhindert zirkuläre Imports durch zentralen Zugriff auf geteilte Monitor-Instanzen.
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
            logger.info(f"📡 [API Monitor] Recorded call from: {source}")

    def get_call_count(self):
        return self.call_count

    def get_elapsed_minutes(self):
        elapsed = datetime.utcnow() - self.start_time
        return max(elapsed.total_seconds() / 60, 1e-6)

    def get_rate_per_minute(self):
        return round(self.call_count / self.get_elapsed_minutes(), 2)

    def get_status_summary(self):
        return (
            f"API Calls: {self.call_count} | "
            f"Duration: {self.get_elapsed_minutes():.1f} min | "
            f"Rate: {self.get_rate_per_minute():.2f}/min"
        )

# === Singleton Export ===
monitor = APIUsageMonitor()

def record_call(source: str = None):
    monitor.record_call(source)
