# Verwende Python 3.8
FROM python:3.8

# Setze das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopiere alle Dateien aus deinem lokalen Verzeichnis in das Container-Verzeichnis
COPY . /app

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Definiere den Befehl zum Starten der App
CMD ["python", "bot.py"]
