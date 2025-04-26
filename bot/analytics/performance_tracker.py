# bot/analytics/performance_tracker.py

"""
Tracks and calculates real-time performance statistics for signals.
"""

performance_data = {
    "total_signals": 0,
    "correct_signals": 0,
    "wrong_signals": 0
}

def update_performance(correct: bool):
    performance_data["total_signals"] += 1
    if correct:
        performance_data["correct_signals"] += 1
    else:
        performance_data["wrong_signals"] += 1

def get_performance_summary() -> str:
    if performance_data["total_signals"] == 0:
        accuracy = 0
    else:
        accuracy = (performance_data["correct_signals"] / performance_data["total_signals"]) * 100

    return (
        f"📈 *Performance Overview*\n\n"
        f"Total Signals: {performance_data['total_signals']}\n"
        f"Correct Signals: {performance_data['correct_signals']}\n"
        f"Wrong Signals: {performance_data['wrong_signals']}\n"
        f"Accuracy: {accuracy:.2f}%\n"
    )
