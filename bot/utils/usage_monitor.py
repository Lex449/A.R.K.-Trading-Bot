# bot/utils/usage_monitor.py

"""
A.R.K. API Usage Monitor – Real-Time NASA-Level Call Tracker.
Monitors API usage per minute to prevent rate limits and overflows.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime

class APIUsageMonitor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.call_count = 0
        self.start_time = datetime.utcnow()

    def record_call(self):
        self.call_count += 1

    def get_call_count(self):
        return self.call_count

    def get_elapsed_minutes(self):
        elapsed = datetime.utcnow() - self.start_time
        return max(elapsed.total_seconds() / 60, 1e-6)  # Prevent division by 0

    def get_rate_per_minute(self):
        return round(self.call_count / self.get_elapsed_minutes(), 2)

    def get_status_summary(self):
        return (
            f"API Calls: {self.call_count} | "
            f"Duration: {self.get_elapsed_minutes():.1f} min | "
            f"Rate: {self.get_rate_per_minute():.2f}/min"
        )

    def log_status(self):
        print(self.get_status_summary())

# Global Singleton Instance
usage_monitor = APIUsageMonitor()
