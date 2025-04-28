# bot/utils/connection_watchdog.py

import requests
import logging
from time import sleep

# URL für die Verbindungstest-Anfrage an die Telegram API (hier wird die `getMe`-Methode verwendet)
CHECK_URL = "https://api.telegram.org/bot<your_bot_token>/getMe"

def check_connection() -> bool:
    """
    Überprüft die Internetverbindung, indem eine Anfrage an die Telegram API gesendet wird.
    Gibt eine Warnung aus, wenn keine Verbindung hergestellt werden kann.
    
    Returns:
        bool: True, wenn die Verbindung erfolgreich ist, False wenn nicht.
    """
    try:
        response = requests.get(CHECK_URL)
        if response.status_code == 200:
            logging.info("✅ Internetverbindung erfolgreich!")
            return True
        else:
            logging.warning(f"⚠️ Verbindung fehlgeschlagen mit Statuscode: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Fehler bei der Verbindung: {e}")
        return False

def start_watchdog():
    """
    Starte den Watchdog, um die Verbindung regelmäßig zu überprüfen.
    Alle 60 Sekunden wird überprüft, ob die Verbindung zum Telegram-Server noch besteht.
    """
    while True:
        if not check_connection():
            logging.warning("❌ Verbindung verloren. Versuche erneut...")
            # Hier könnte ein Alarm an den Benutzer gesendet werden, oder eine Wiederverbindung ausgelöst werden
        sleep(60)  # Überprüfe alle 60 Sekunden
