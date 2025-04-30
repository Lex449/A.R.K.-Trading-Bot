# bot/engine/data_loader.py

"""
A.R.K. Data Loader – Ultra Resilient Dual Source Market Fetcher 7.0
Primary: Finnhub API | Secondary: Yahoo Finance Backup
Optimiert für maximale Signaldichte und Fehlerrobustheit.

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
from bot.utils.api_bridge import record_call

# Logger & Settings
logger = setup_logger(__name__)
config = get_settings()
FINNHUB_TOKEN = config.get("FINNHUB_API_KEY")

async def fetch_market_data(symbol: str, chat_id: int = None) -> pd.DataFrame | None:
    """
    Fetches OHLCV historical data.
    Priority: Finnhub → Fallback: Yahoo Finance

    Returns:
        pd.DataFrame or None
    """
    lang = get_language(chat_id) if chat_id else "en"
    finnhub_url = (
        f"https://finnhub.io/api/v1/stock/candle"
        f"?symbol={symbol}&resolution=5&count=300&token={FINNHUB_TOKEN}"
    )

    # === Attempt 1: Finnhub ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_primary', lang)} {symbol}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(finnhub_url, timeout=10) as response:
                if response.status != 200:
                    raise ConnectionError(f"Finnhub HTTP {response.status}")
                data = await response.json()

        if data.get("s") != "ok":
            raise ValueError(f"Finnhub error status: {data.get('s')}")

        required_keys = {"o", "h", "l", "c", "v", "t"}
        if not required_keys.issubset(data.keys()):
            raise KeyError(f"Finnhub missing keys: {required_keys - data.keys()}")

        df = pd.DataFrame({
            "t": pd.to_datetime(data["t"], unit="s"),
            "o": data["o"],
            "h": data["h"],
            "l": data["l"],
            "c": data["c"],
            "v": data["v"]
        }).set_index("t")

        if df.empty or len(df) < 20 or df["c"].tail(10).nunique() <= 1:
            raise ValueError("Finnhub returned flat or insufficient data")

        record_call()
        logger.info(f"✅ [DataLoader] Finnhub success: {symbol}")
        return df.astype(float)

    except Exception as e_primary:
        logger.warning(f"⚠️ [DataLoader] {get_text('error_primary_source', lang)} {symbol}: {e_primary}")

    # === Attempt 2: Yahoo Finance ===
    try:
        logger.info(f"[DataLoader] {get_text('fetching_data_backup', lang)} {symbol}...")
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")

        if hist.empty or len(hist) < 20 or hist["Close"].tail(10).nunique() <= 1:
            raise ValueError("Yahoo Finance returned insufficient or flat data")

        hist = hist.rename(columns={
            "Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"
        })

        df = hist[["o", "h", "l", "c", "v"]].copy()
        df.index.name = "t"
        logger.info(f"✅ [DataLoader] Yahoo fallback used: {symbol}")
        return df.astype(float)

    except Exception as e_backup:
        logger.error(f"❌ [DataLoader] {get_text('error_backup_source', lang)} {symbol}: {e_backup}")
        return None
