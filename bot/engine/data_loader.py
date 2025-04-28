"""
A.R.K. Data Loader – Dual Source Market Fetcher Ultra 3.0
Primary: Finnhub API | Backup: Yahoo Finance
Maximal Fault-Tolerant, Ultra-Optimized, Multilingual Logging.
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

# Finnhub API Key
FINNHUB_TOKEN = config.get("FINNHUB_API_KEY")

async def fetch_market_data(symbol: str, chat_id: int = None) -> pd.DataFrame | None:
    """
    Fetches historical OHLCV data for a symbol.
    Priority: Finnhub → Backup: Yahoo Finance.

    Args:
        symbol (str): Ticker symbol (e.g., AAPL, TSLA).
        chat_id (int, optional): For user-specific language messages.

    Returns:
        pd.DataFrame or None if both sources fail.
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
                        raise ValueError(f"Invalid Finnhub Response: {data}")

                    df = pd.DataFrame({
                        "t": pd.to_datetime(data["t"], unit="s"),
                        "o": data["o"],
                        "h": data["h"],
                        "l": data["l"],
                        "c": data["c"],
                        "v": data["v"],
                    }).set_index("t")

                    logger.info(f"[DataLoader] ✅ Finnhub data fetched successfully for {symbol}.")
                    return df

                else:
                    raise ConnectionError(f"Finnhub HTTP Error: {response.status}")

    except Exception as primary_error:
        logger.warning(f"[DataLoader] {get_text('error_primary_source', lang)}: {primary_error}")

    # === Fallback to Backup Source: Yahoo Finance ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_backup', lang)}")

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")

        if hist.empty:
            raise ValueError("Yahoo Finance returned empty dataset.")

        hist = hist.rename(columns={
            "Open": "o",
            "High": "h",
            "Low": "l",
            "Close": "c",
            "Volume": "v"
        })

        df = hist[["o", "h", "l", "c", "v"]]

        logger.info(f"[DataLoader] ✅ Yahoo Finance data fetched successfully for {symbol}.")
        return df

    except Exception as backup_error:
        logger.error(f"[DataLoader] {get_text('error_backup_source', lang)}: {backup_error}")
        return None
