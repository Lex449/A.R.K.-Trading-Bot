import os
from dotenv import load_dotenv

# Lädt die .env-Datei
load_dotenv()

def get_settings():
    return {
        "TOKEN": os.getenv("7655719634:AAE01VP0eZP3gQGXgiL_hHOgBD3pG5yzId4"),
        "DANIEL_ID": os.getenv("7699862580"),
        "TWELVEDATA_KEY": os.getenv("0dd4ddf44b144ea48df01c9fdfc80921")
    }