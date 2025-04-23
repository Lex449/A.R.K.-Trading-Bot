# bot/auto/signals.py
# Modul für automatische Signalgenerierung und Senden an Abonnenten

from datetime import datetime
from bot.config import config
from bot.utils import analysis

# Globale Variablen für Abonnenten und Signal-Historie
subscribers = set()
signals_sent_count = 0
last_signals = {}  # z.B. {"US100": {"direction": "LONG", "time": datetime}}

# Zeitpunkt des Bot-Starts (wird in main.py gesetzt)
start_time = None

def subscribe(chat_id: int):
    """Fügt einen Chat zu den Signal-Abonnenten hinzu."""
    subscribers.add(chat_id)

def unsubscribe(chat_id: int):
    """Entfernt einen Chat aus den Signal-Abonnenten."""
    subscribers.discard(chat_id)

def send_signals_job(context):
    """Wird periodisch aufgerufen. Prüft alle Indizes und sendet neue Signale an Abonnenten."""
    global signals_sent_count
    results = []
    for symbol_name in config.SYMBOLS.keys():
        res = analysis.analyze_symbol(symbol_name)
        if res is None:
            continue  # Überspringen, falls Daten nicht abrufbar
        if res.get("signal"):
            results.append((symbol_name, res["signal"]))
            # Statistik aktualisieren
            signals_sent_count += 1
            last_signals[symbol_name] = {"direction": res["signal"], "time": datetime.now()}
    if not results:
        return  # Keine neuen Signale in diesem Durchlauf
    # Text für die Nachricht zusammenbauen
    parts = [f"{name}: {sig}" for name, sig in results]
    if len(parts) == 1:
        message_text = f"Signal: {parts[0]}"
    else:
        message_text = "Signale: " + "; ".join(parts)
    # An alle Abonnenten senden
    for chat_id in list(subscribers):
        try:
            context.bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as e:
            print(f"[FEHLER] Senden der Signale an Chat {chat_id} fehlgeschlagen: {e}")
