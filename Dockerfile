FROM python:3.8-slim  # Hier setzen wir Python 3.8, aber es kann auch 3.9 oder 3.7 sein, je nach Bedarf

# Setzt das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopiere alle Dateien ins Arbeitsverzeichnis
COPY . /app

# Installiere alle Abhängigkeiten aus requirements.txt
RUN pip install -r requirements.txt

# Starte das Projekt (Beispiel: run.py)
CMD ["python", "run.py"]
