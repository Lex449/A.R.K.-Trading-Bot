def map_symbol(symbol: str, fallback: bool = False) -> str:
    """
    Wandelt interne Symbolnamen in Finnhub- oder Yahoo-kompatible Kürzel um.
    """
    mappings = {
        "US100": "NDX",     # Nasdaq 100
        "US30": "DJI",      # Dow Jones
        "SPX500": "SPX",    # S&P 500
        "IWM": "IWM",       # Russell 2000 ETF
        "QQQ": "QQQ",       # Nasdaq ETF
        "DIA": "DIA",       # Dow Jones ETF
        "MDY": "MDY"        # MidCap 400 ETF
    }

    yahoo_fallback = {
        "US100": "^NDX",
        "US30": "^DJI",
        "SPX500": "^GSPC",
        "IWM": "IWM",
        "QQQ": "QQQ",
        "DIA": "DIA",
        "MDY": "MDY"
    }

    if fallback:
        return yahoo_fallback.get(symbol, symbol)
    return mappings.get(symbol, symbol)
