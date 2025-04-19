import requests
import pandas as pd
from bot.config import API_KEY

def fetch_market_data(symbol: str, interval: str, start_date: str, end_date: str):
    url = f'https://api.twelvedata.com/time_series'
    params = {
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY,
        'start_date': start_date,
        'end_date': end_date,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'values' in data:
        # Umwandlung der Daten in DataFrame
        df = pd.DataFrame(data['values'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df.astype(float)  # Konvertiere alle Daten in Floats für TA-Lib
        return df
    else:
        raise ValueError("Fehler beim Abrufen der Marktdaten")