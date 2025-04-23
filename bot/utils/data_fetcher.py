# bot/utils/data_fetcher.py

import requests
import pandas as pd
from bot.config.settings import get_settings

def fetch_market_data(symbol: str, interval: str = "5min", start_date: str = None, end_date: str = None):
    """Holt Marktdaten von der TwelveData API für ein gegebenes Symbol."""
    settings = get_settings()
    api_key = settings["TWELVEDATA_API_KEY"]

    url = f'https://api.twelvedata.com/time_series'
    params = {
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key,
        'start_date': start_date,
        'end_date': end_date,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'values' in data:
        df = pd.DataFrame(data['values'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df.astype(float)
        return df
    else:
        raise ValueError("Fehler beim Abrufen der Marktdaten oder ungültiges Symbol.")
