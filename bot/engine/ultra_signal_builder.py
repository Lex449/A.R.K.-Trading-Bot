# bot/engine/ultra_signal_builder.py

"""
A.R.K. Ultra Signal Builder – Combines all detections into premium multilingual messages.
Designed for: Premium Signal Outputs, Ultra Clarity, Motivational Edge.
"""

def build_ultra_signal(symbol: str, move: dict, volume_spike: dict, atr_breakout: dict, risk_reward: dict, lang: str = "en") -> str:
    """
    Builds the ultimate multilingual premium trading signal message.

    Args:
        symbol (str): Trading symbol.
        move (dict): Move Detection result (required).
        volume_spike (dict): Volume Spike Detection result (optional).
        atr_breakout (dict): ATR Breakout Detection result (optional).
        risk_reward (dict): Risk/Reward analysis result (required).
        lang (str): Language code ("en" or "de").

    Returns:
        str: Complete formatted signal message.
    """

    if not move or not risk_reward:
        return ""  # Critical components missing

    # Language Templates
    templates = {
        "en": {
            "title": "🚨 Strong Move Detected!",
            "symbol": "*Symbol:*",
            "movement": "*Movement:*",
            "volume": "*Volume Spike:*",
            "atr": "*ATR Breakout:*",
            "trend": "*Trend:*",
            "confidence": "🧠 Stay sharp – strategy rules!",
            "long": "📈 Long",
            "short": "📉 Short",
            "rr": "*Risk/Reward Analysis:*",
        },
        "de": {
            "title": "🚨 Starker Marktalarm!",
            "symbol": "*Symbol:*",
            "movement": "*Bewegung:*",
            "volume": "*Volumen Spike:*",
            "atr": "*ATR-Ausbruch:*",
            "trend": "*Trend:*",
            "confidence": "🧠 Selbstvertrauen hoch halten – Strategie bleibt König!",
            "long": "📈 Long",
            "short": "📉 Short",
            "rr": "*Risiko/Ertrags Analyse:*",
        }
    }

    t = templates.get(lang.lower(), templates["en"])  # fallback to English if unknown

    # Message Parts
    parts = [
        t["title"],
        f"{t['symbol']} `{symbol}`",
        f"{t['movement']} `{move['move_percent']:.2f}%`",
        f"{t['volume']} `{volume_spike['volume_percent']:.1f}%`" if volume_spike else "",
        f"{t['atr']} `{atr_breakout['atr_ratio']:.1f}%`" if atr_breakout else "",
        f"{t['trend']} {t['long'] if move['direction'] == 'long' else t['short']}",
        f"{t['rr']} ➔ Target `{risk_reward['target']}` | Stop `{risk_reward['stop_loss']}` | R/R `{risk_reward['risk_reward_ratio']}x`",
        f"\n{t['confidence']}"
    ]

    return "\n".join([p for p in parts if p])
