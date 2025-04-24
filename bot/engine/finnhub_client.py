# bot/engine/finnhub_client.py
import os
import finnhub
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_finnhub_client():
    return finnhub.Client(api_key=FINNHUB_API_KEY)
