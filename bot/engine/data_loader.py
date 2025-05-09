"""
A.R.K. Data Loader – Ultra Precision Finnhub Priority Build 7.3
Exklusiver Fokus auf Finnhub: Multi-Resolution Pathing, Logging jeder Abweichung.
Validierung ausgelagert an data_auto_validator.py.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import aiohttp
import yfinance as yf
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.api_bridge import record_call

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()
FINNHUB_TOKEN = config.get("FINNHUB_API_KEY")

# === Finnhub API Call ===
async def fetch_from_finnhub(symbol: str, resolution: str) -> pd.DataFrame:
    url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution={resolution}&count=300&token={FINNHUB_TOKEN}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                raise ConnectionError(f"Finnhub HTTP {response.status} – {symbol} ({resolution}m)")

            data = await response.json()
            if data.get("s") != "ok" or not all(k in data for k in ["o", "h", "l", "c", "v", "t"]):
                raise ValueError(f"Finnhub response malformed for {symbol} ({resolution}m)")

            df = pd.DataFrame({
                "t": pd.to_datetime(data["t"], unit="s"),
                "o": data["o"],
                "h": data["h"],
                "l": data["l"],
                "c": data["c"],
                "v": data["v"]
            }).set_index("t")

            logger.info(
                f"✅ [Finnhub] {symbol} | {resolution}m | Rows: {len(df)} | "
                f"Recent: {df['c'].tail(3).tolist()}"
            )

            record_call(symbol)
            return df.astype(float)

# === Entry Function for Analysis Engine ===
async def fetch_market_data(symbol: str, chat_id: int = None) -> pd.DataFrame | None:
    lang = get_language(chat_id) if chat_id else "en"

    # 1. Finnhub 5-Minuten
    try:
        logger.info(f"⏳ [DataLoader] {get_text('fetching_data_primary', lang)} {symbol} (5m)")
        return await fetch_from_finnhub(symbol, "5")
    except Exception as e1:
        logger.warning(f"⚠️ [DataLoader] Finnhub 5m failed → {symbol}: {e1}")

    # 2. Finnhub 15-Minuten Fallback
    try:
        logger.info(f"⏳ [DataLoader] Retrying {symbol} with 15m fallback...")
        return await fetch_from_finnhub(symbol, "15")
    except Exception as e2:
        logger.warning(f"⚠️ [DataLoader] Finnhub 15m failed → {symbol}: {e2}")

    # 3. Yahoo Finance Backup (letzte Chance)
    try:
        logger.info(f"⏳ [DataLoader] {get_text('fetching_data_backup', lang)} {symbol} (Yahoo Fallback)")
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")

        hist = hist.rename(columns={
            "Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"
        })

        df = hist[["o", "h", "l", "c", "v"]].copy()
        df.index.name = "t"

        logger.info(
            f"✅ [YahooBackup] {symbol} fallback used | Rows: {len(df)} | "
            f"Recent: {df['c'].tail(3).tolist()}"
        )

        return df.astype(float)

    except Exception as e3:
        logger.error(
            f"❌ [DataLoader] {get_text('error_backup_source', lang)} {symbol}: {e3}"
        )
        return None
