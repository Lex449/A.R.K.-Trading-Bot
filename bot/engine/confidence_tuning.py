# bot/engine/confidence_tuning.py

"""
Adaptive Confidence Tuning Modul
A.R.K. passt automatisch die Signal-Confidence basierend auf Performance-Daten an.
"""

def tune_confidence(signal_data: dict, session_stats: dict) -> dict:
    """
    Passt die Confidence eines Signals dynamisch an, basierend auf vergangener Erfolgsrate.

    Args:
        signal_data (dict): Aktuelles Signal inkl. ursprünglicher Confidence.
        session_stats (dict): Statistikdaten der aktuellen Session (z.B. Win-Rate).

    Returns:
        dict: Signal mit adaptierter Confidence.
    """

    # Basis: ursprüngliche Confidence
    original_confidence = signal_data.get("confidence", 0.5)

    # Berechnung: Win-Rate aus Session-Daten
    total_signals = session_stats.get("signals_total", 1)  # Vermeidet Division durch 0
    strong_signals = session_stats.get("strong_signals", 0)

    win_rate = strong_signals / total_signals

    # Tuning-Logik
    if win_rate > 0.7:
        adjustment = 0.1  # Verstärken bei starker Performance
    elif win_rate < 0.4:
        adjustment = -0.1  # Abschwächen bei schwacher Performance
    else:
        adjustment = 0.0  # Keine Anpassung bei normaler Performance

    # Neue Confidence berechnen
    tuned_confidence = original_confidence + adjustment

    # Begrenzung: 0.1 <= confidence <= 0.9
    tuned_confidence = max(0.1, min(0.9, tuned_confidence))

    # Aktualisiertes Signal zurückgeben
    signal_data["confidence"] = round(tuned_confidence, 2)

    return signal_data
