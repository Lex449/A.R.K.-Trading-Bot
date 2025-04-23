# bot/utils/error_handler.py

import logging

# Fehlerbehandlung für den Bot
def handle_error(update, context):
    """Funktion zur Fehlerbehandlung in Telegram Bot."""
    error = context.error
    logging.error(f"Fehler aufgetreten: {error}")

    # Zusätzliche Fehlerbehandlung, falls nötig
    try:
        # Schicke eine Benachrichtigung an den Administrator
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"❗️Es gab einen Fehler beim Ausführen des Befehls. Der Fehler wird protokolliert. Fehlerdetails: {error}"
        )
    except Exception as e:
        logging.error(f"Fehler bei der Fehlerbenachrichtigung: {e}")
