# bot/engine/symbol_map.py

def map_symbol(symbol: str, fallback: bool = False) -> str:
    """
    Wandelt interne Symbolnamen in Finnhub oder Yahoo-kompatible Kürzel um.
    """
    mappings = {
        "US100": "NDX",
        "US30": "DJI",
        "DE40": "^GDAXI",
        "JP225": "^N225",
        "HK50": "^HSI",
        "SPX500": "SPX"
    }

    yahoo_fallback = {
        "US100": "^NDX",
        "US30": "^DJI",
        "DE40": "^GDAXI",
        "JP225": "^N225",
        "HK50": "^HSI",
        "SPX500": "^GSPC"
    }

    if fallback:
        return yahoo_fallback.get(symbol, symbol)
    return mappings.get(symbol, symbol)
