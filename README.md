# A.R.K. Trading Bot

A.R.K. ist ein Trading-Bot, der Marktsignale analysiert und automatisch eingehende Handelssignale versendet. Der Bot ist für den Einsatz auf Telegram entwickelt und bietet ein zweisprachiges Interface in Deutsch und Englisch.

## Features

- **Marktanalyse:** Der Bot führt automatische Marktanalysen durch und erkennt Trading-Muster.
- **Benachrichtigungen:** Automatische Benachrichtigungen über aktuelle Handelssignale.
- **Mehrsprachig:** Der Bot unterstützt Deutsch und Englisch.

## Installation

1. Klone das Repository:
    ```bash
    git clone https://github.com/DEIN_BOT_REPOSITORY.git
    ```

2. Installiere die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

3. Erstelle eine `.env`-Datei mit den folgenden Variablen:
    ```
    BOT_TOKEN=DEIN_BOT_TOKEN
    DANIEL_TELEGRAM_ID=DEIN_TELEGRAM_ID
    TWELVEDATA_API_KEY=DEIN_API_KEY
    ```

4. Starte den Bot:
    ```bash
    python main.py
    ```

## Nutzung

- **/start:** Startet den Bot und zeigt eine Begrüßungsnachricht.
- **/ping:** Überprüft, ob der Bot online ist.
- **/status:** Zeigt den aktuellen Status des Bots an.
- **/signal:** Zeigt das aktuelle Marktsignal basierend auf der Analyse.
- **/shutdown:** Stoppt den Bot (nur für autorisierte Benutzer).