import logging
import requests

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_updates_from_telegram(bot_token):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.post(url)
        
        # Logs für die Antwort
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            updates = response.json()
            logger.debug(f"Updates: {updates}")
            return updates
        else:
            logger.error(f"Fehler beim Abrufen der Updates: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Fehler bei getUpdates: {e}")
        return None
