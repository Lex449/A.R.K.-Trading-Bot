# bot/engine/symbol_map.py

def map_symbol(symbol: str, fallback: bool = False) -> str:
    """
    Konvertiert interne Symbolnamen in API-kompatible Kürzel.
    
    - Standard: Finnhub-kompatibel (keine Prefixes)
    - Fallback: Yahoo Finance-kompatibel (mit ^ für Indices)

    Args:
        symbol (str): Interner Symbolname (z. B. "US100")
        fallback (bool): True → Yahoo Symbol; False → Finnhub Symbol

    Returns:
        str: API-kompatibler Symbolname
    """

    # Finnhub-kompatible Kürzel (z. B. für kostenpflichtige Indizes mit Pro-Plan)
    finnhub_map = {
        "US100": "NDX",      # Nasdaq 100 Index
        "US30": "DJI",       # Dow Jones Industrial Average
        "DE40": "^GDAXI",    # DAX
        "JP225": "^N225",    # Nikkei 225
        "HK50": "^HSI",      # Hang Seng
        "SPX500": "SPX"      # S&P 500 (Symbol kann je nach API variieren)
    }

    # Yahoo-kompatible Kürzel für Fallback mit yfinance
    yahoo_map = {
        "US100": "^NDX",
        "US30": "^DJI",
        "DE40": "^GDAXI",
        "JP225": "^N225",
        "HK50": "^HSI",
        "SPX500": "^GSPC"
    }

    mapping = yahoo_map if fallback else finnhub_map
    return mapping.get(symbol, symbol)
