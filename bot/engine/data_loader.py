"""
A.R.K. Data Loader – Dual Source Market Fetcher.
Primary: Finnhub API
Backup: Yahoo Finance
Optimized for fault tolerance, speed, and multilingual logging.
"""

import pandas as pd
import logging
import aiohttp
import yfinance as yf
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

FINNHUB_TOKEN = config.get("FINNHUB_API_KEY")

async def fetch_market_data(symbol: str, chat_id: int = None) -> pd.DataFrame:
    """
    Fetches historical OHLC data for a symbol from Finnhub.
    Falls back to Yahoo Finance if Finnhub fails.

    Args:
        symbol (str): Ticker symbol (e.g., AAPL, TSLA).
        chat_id (int, optional): User's chat ID for language detection.

    Returns:
        pd.DataFrame or None
    """
    lang = get_language(chat_id) if chat_id else "en"

    # === Try Primary Source: Finnhub ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_primary', lang)}")

        async with aiohttp.ClientSession() as session:
            url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=5&count=300&token={FINNHUB_TOKEN}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("s") != "ok":
                        raise ValueError(f"Finnhub response invalid: {data}")

                    df = pd.DataFrame({
                        "t": pd.to_datetime(data["t"], unit="s"),
                        "o": data["o"],
                        "h": data["h"],
                        "l": data["l"],
                        "c": data["c"],
                        "v": data["v"],
                    })

                    df = df[["t", "o", "h", "l", "c", "v"]]
                    df.set_index("t", inplace=True)
                    logger.info(f"[DataLoader] Finnhub data fetched successfully for {symbol}.")
                    return df
                else:
                    raise Exception(f"HTTP {response.status}")

    except Exception as e:
        logger.warning(f"[DataLoader] {get_text('error_primary_source', lang)}: {e}")

    # === Backup Source: Yahoo Finance ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_backup', lang)}")

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")

        if hist.empty:
            raise ValueError("Yahoo Finance returned empty data.")

        hist = hist.rename(columns={
            "Open": "o",
            "High": "h",
            "Low": "l",
            "Close": "c",
            "Volume": "v"
        })

        df = hist[["o", "h", "l", "c", "v"]]
        logger.info(f"[DataLoader] Yahoo Finance data fetched successfully for {symbol}.")
        return df

    except Exception as e:
        logger.error(f"[DataLoader] {get_text('error_backup_source', lang)}: {e}")
        return None
