FROM python:3.8-slim  # Ändere hier auf die gewünschte Version, z.B. python:3.8-slim

# Setzt das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopiere alle Dateien ins Arbeitsverzeichnis
COPY . /app

# Installiere alle Abhängigkeiten aus requirements.txt
RUN pip install -r requirements.txt

# Starte das Projekt (Beispiel: run.py)
CMD ["python", "run.py"]
