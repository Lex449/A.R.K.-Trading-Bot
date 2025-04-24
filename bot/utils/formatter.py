def format_signal(symbol: str, trend: str, confidence: float, pattern: str, lang: str) -> str:
    stars = "⭐️" * round(confidence)

    names_en = {
        "US100": "NASDAQ 100",
        "US30": "Dow Jones",
        "SPX500": "S&P 500",
        "IWM": "Russell 2000",
        "QQQ": "NASDAQ ETF",
        "DIA": "Dow ETF",
        "MDY": "MidCap 400"
    }

    names_de = {
        "US100": "NASDAQ 100",
        "US30": "Dow Jones",
        "SPX500": "S&P 500",
        "IWM": "Russell 2000",
        "QQQ": "NASDAQ ETF",
        "DIA": "Dow ETF",
        "MDY": "MidCap 400"
    }

    name = names_de.get(symbol, symbol) if lang == "de" else names_en.get(symbol, symbol)

    if lang == "de":
        return (
            f"📊 *{name}*\n"
            f"Trend: *{trend.upper()}*\n"
            f"Zuversicht: {stars} ({round(confidence, 2)}/5)\n"
            f"Signalmuster: `{pattern}`"
        )
    else:
        return (
            f"📊 *{name}*\n"
            f"Trend: *{trend.upper()}*\n"
            f"Confidence: {stars} ({round(confidence, 2)}/5)\n"
            f"Pattern: `{pattern}`"
        )
