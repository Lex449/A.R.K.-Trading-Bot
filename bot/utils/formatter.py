# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: float, pattern: str, lang: str = "en") -> str:
    stars = "⭐️" * round(confidence) + "✩" * (5 - round(confidence))

    names_en = {
        "US100": "NASDAQ 100",
        "US30": "Dow Jones",
        "SPX500": "S&P 500",
        "JP225": "Nikkei 225",
        "HK50": "Hang Seng",
        "DE40": "DAX 40"
    }

    names_de = {
        "US100": "NASDAQ 100",
        "US30": "Dow Jones",
        "SPX500": "S&P 500",
        "JP225": "Nikkei 225",
        "HK50": "Hang Seng",
        "DE40": "DAX 40"
    }

    display_name = names_de.get(symbol, symbol) if lang == "de" else names_en.get(symbol, symbol)

    if lang == "de":
        return (
            f"📊 *{display_name}*\n"
            f"Trend: *{trend.upper()}*\n"
            f"Zuversicht: {stars} ({round(confidence, 1)}/5)\n"
            f"Signalmuster: `{pattern}`"
        )
    else:
        return (
            f"📊 *{display_name}*\n"
            f"Trend: *{trend.upper()}*\n"
            f"Confidence: {stars} ({round(confidence, 1)}/5)\n"
            f"Pattern: `{pattern}`"
        )
