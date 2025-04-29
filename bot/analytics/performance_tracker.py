"""
A.R.K. Performance Tracker – Ultra Premium Live Monitoring & Recap Engine 2025.
Tracks real-time signal quality, average confidence, strong accuracy.
Provides full daily and weekly recaps. Auto-backup included.
"""

import json
import os
from datetime import datetime
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text

# Setup structured logger
logger = setup_logger(__name__)

# Performance Storage
PERFORMANCE_FILE = "performance_data.json"

# In-Memory Data
performance_data = {
    "session_start": datetime.utcnow().isoformat(),
    "total_signals": 0,
    "strong_signals": 0,
    "moderate_signals": 0,
    "weak_signals": 0,
    "total_confidence": 0.0,
}

# Load previous session if exists
if os.path.exists(PERFORMANCE_FILE):
    try:
        with open(PERFORMANCE_FILE, "r", encoding="utf-8") as f:
            performance_data.update(json.load(f))
        logger.info("✅ [PerformanceTracker] Loaded existing performance session.")
    except Exception as e:
        logger.warning(f"⚠️ [PerformanceTracker] Failed loading previous performance data: {e}")

# === Core Tracking Functions ===

def update_performance(stars: int, confidence: float):
    """
    Updates performance stats with new signal.
    """
    performance_data["total_signals"] += 1
    performance_data["total_confidence"] += confidence

    if stars >= 5:
        performance_data["strong_signals"] += 1
        logger.info(f"✅ [Performance] 5⭐ Elite Signal | {confidence:.1f}% Confidence")
    elif stars == 4:
        performance_data["moderate_signals"] += 1
        logger.info(f"⚡ [Performance] 4⭐ Good Signal | {confidence:.1f}% Confidence")
    else:
        performance_data["weak_signals"] += 1
        logger.info(f"⚠️ [Performance] Weak Signal ({stars}⭐) | {confidence:.1f}% Confidence")

    _save_performance_data()

def _save_performance_data():
    """Internal: Save to file."""
    try:
        with open(PERFORMANCE_FILE, "w", encoding="utf-8") as f:
            json.dump(performance_data, f, indent=4)
        logger.info("💾 [Performance] Saved current performance data.")
    except Exception as e:
        logger.error(f"❌ [Performance] Failed to save: {e}")

# === Recap Builders ===

def generate_daily_recap() -> str:
    """
    Generates today's recap based on session start.
   
