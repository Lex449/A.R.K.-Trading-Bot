"""
A.R.K. Data Loader – Real-Time Market Data Fetcher.
Handles clean OHLCV data retrieval for precision analysis.
"""

import yfinance as yf
import pandas as pd

async def fetch_market_data(symbol: str, period: str = "7d", interval: str = "15m") -> pd.DataFrame:
    """
    Fetches OHLCV market data for a given symbol.

    Args:
        symbol (str): The trading symbol (e.g., "AAPL", "TSLA").
        period (str): Data period (e.g., "7d", "1mo").
        interval (str): Candle interval (e.g., "15m", "1h").

    Returns:
        pd.DataFrame or None: Market data or None on error.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)

        if df is None or df.empty:
            return None

        df = df.rename(columns={
            "High": "h",
            "Low": "l",
            "Close": "c",
            "Open": "o",
            "Volume": "v"
        })

        return df[["o", "h", "l", "c", "v"]]

    except Exception:
        return None
