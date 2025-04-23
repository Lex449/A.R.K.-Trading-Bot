import os
from dotenv import load_dotenv

# ENV laden (nur lokal/replit, Railway lädt automatisch)
load_dotenv()

def get_settings():
    """Perfekte, stabile Live-Einstellungen für A.R.K. Trading Bot."""
    return {
        # Telegram
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),

        # TwelveData API
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),

        # Symbol-Übersetzung für User-Kommandos
        "SYMBOLS": {
            "QQQ": "QQQ",    # Nasdaq-100 ETF
            "SPY": "SPY",    # S&P 500 ETF
            "DIA": "DIA",    # Dow Jones ETF
            "IWM": "IWM",    # Russell 2000 ETF
            "MDY": "MDY",    # S&P MidCap 400 ETF
            "US100": "NDX",  # Nasdaq-100 Index
            "US30": "DJI",   # Dow Jones Index
            "SPX500": "SPX", # S&P 500 Index
            "DAX": "DAX",    # Deutscher Leitindex
        },

        # Analyse-