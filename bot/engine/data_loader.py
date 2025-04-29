"""
A.R.K. Data Loader – Ultra Resilient Dual Source Market Fetcher 5.0
Primary: Finnhub API | Secondary: Yahoo Finance Backup
Unbreakable Real-Time Data Integrity Engine. Multilingual Safety Reporting. 

Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import logging
import aiohttp
import yfinance as yf
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Logger & Settings
logger = setup_logger(__name__)
config = get_settings()
FINNHUB_TOKEN = config.get("FINNHUB_API_KEY")

async def fetch_market_data(symbol: str, chat_id: int = None) -> pd.DataFrame | None:
    """
    Fetches OHLCV historical data.
    Priority: Finnhub → Backup: Yahoo Finance.

    Args:
        symbol (str): Trading symbol (e.g., AAPL).
        chat_id (int, optional): User's chat ID for language-specific logging.

    Returns:
        pd.DataFrame or None
    """
    lang = get_language(chat_id) if chat_id else "en"

    # === Attempt 1: Finnhub Primary Source ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_primary', lang)} {symbol}...")

        async with aiohttp.ClientSession() as session:
            url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=5&count=300&token={FINNHUB_TOKEN}"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()

                    if data.get("s") != "ok" or not data.get("c"):
                        raise ValueError(f"Invalid Finnhub response structure: {data}")

                    df = pd.DataFrame({
                        "t": pd.to_datetime(data["t"], unit="s"),
                        "o": data["o"],
                        "h": data["h"],
                        "l": data["l"],
                        "c": data["c"],
                        "v": data["v"],
                    }).set_index("t")

                    if df.empty or len(df) < 20:
                        raise ValueError("Finnhub returned insufficient data points.")

                    logger.info(f"✅ [DataLoader] Finnhub data loaded successfully for {symbol}.")
                    return df

                raise ConnectionError(f"Finnhub API error: HTTP {response.status}")

    except Exception as e_primary:
        logger.warning(f"⚠️ [DataLoader] {get_text('error_primary_source', lang)}: {e_primary}")

    # === Attempt 2: Yahoo Finance Backup ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_backup', lang)} {symbol}...")

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")

        if hist.empty or len(hist) < 20:
            raise ValueError("Yahoo Finance returned insufficient historical data.")

        hist = hist.rename(columns={
            "Open": "o",
            "High": "h",
            "Low": "l",
            "Close": "c",
            "Volume": "v"
        })

        df = hist[["o", "h", "l", "c", "v"]]

        logger.info(f"✅ [DataLoader] Yahoo Finance data loaded successfully for {symbol}.")
        return df

    except Exception as e_backup:
        logger.error(f"❌ [DataLoader] {get_text('error_backup_source', lang)}: {e_backup}")
        return None
