FROM python:3.10-slim

WORKDIR /app
COPY . .

# Hier requirements.txt explizit erwähnen, zur Sicherheit:
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]