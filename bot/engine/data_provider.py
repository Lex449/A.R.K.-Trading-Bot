def get_candles_finnhub(symbol: str, interval: str = "5", limit: int = 100):
    mapped = map_symbol(symbol)
    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": mapped,
        "resolution": interval,
        "count": limit,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG] Finnhub Request for {symbol} returned {response.status_code}: {response.text}")
        data = response.json()

        if data.get("s") != "ok":
            raise Exception(f"Finnhub returned status {data.get('s')}")

        return [{
            "timestamp": data["t"][i],
            "open": data["o"][i],
            "high": data["h"][i],
            "low": data["l"][i],
            "close": data["c"][i]
        } for i in range(len(data["t"]))]

    except Exception as e:
        print(f"[ERROR] Finnhub API failed: {e}")
        return []
