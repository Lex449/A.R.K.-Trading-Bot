# Benutze ein leichtes Python-Image
FROM python:3.8-slim

# Setzt das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere alle Dateien aus deinem lokalen Verzeichnis ins Container-Arbeitsverzeichnis
COPY . /app

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Definiere den Befehl zum Starten der App
CMD ["python", "bot.py"]
