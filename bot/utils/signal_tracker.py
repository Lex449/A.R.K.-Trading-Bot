import datetime

# Memory cache for today's signals
_signal_count = 0
_confidence_total = 0.0
_today = datetime.date.today()

def track_signal(confidence: float):
    global _signal_count, _confidence_total, _today
    now = datetime.date.today()
    if now != _today:
        _signal_count = 0
        _confidence_total = 0.0
        _today = now
    _signal_count += 1
    _confidence_total += confidence

def get_signal_count() -> int:
    return _signal_count

def get_avg_confidence() -> float:
    return round(_confidence_total / _signal_count, 2) if _signal_count else 0.0
