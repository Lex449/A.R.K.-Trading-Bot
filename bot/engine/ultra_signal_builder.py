"""
A.R.K. Ultra Signal Builder – Combines all detections into premium messages.
"""

def build_ultra_signal(symbol, move, volume_spike, atr_breakout, risk_reward, lang="en"):
    """
    Builds the ultimate signal message.
    Args:
        symbol (str): Trading symbol.
        move (dict): Move Detection result.
        volume_spike (dict): Volume Detection result.
        atr_breakout (dict): ATR Detection result.
        risk_reward (str): Risk/Reward text.
        lang (str): "en" or "de"

    Returns:
        str
    """
    if lang == "de":
        title = "🚨 Starker Marktalarm!"
        movement = f"*Bewegung:* `{move['move_percent']:.2f}%`"
        volume = f"*Volumen Spike:* `{volume_spike['volume_percent']:.1f}%` über normal" if volume_spike else ""
        atr = f"*ATR-Ausbruch:* `{atr_breakout['atr_ratio']:.1f}%` größer" if atr_breakout else ""
        trend = "📈 Long" if move["direction"] == "long" else "📉 Short"
        confidence = "Selbstvertrauen hoch halten – Strategie bleibt König!"
    else:
        title = "🚨 Strong Move Detected!"
        movement = f"*Movement:* `{move['move_percent']:.2f}%`"
        volume = f"*Volume Spike:* `{volume_spike['volume_percent']:.1f}%` above normal" if volume_spike else ""
        atr = f"*ATR Breakout:* `{atr_breakout['atr_ratio']:.1f}%` larger" if atr_breakout else ""
        trend = "📈 Long" if move["direction"] == "long" else "📉 Short"
        confidence = "Stay sharp – strategy rules!"

    parts = [
        title,
        f"*Symbol:* `{symbol}`",
        movement,
        volume,
        atr,
        f"*Trend:* {trend}",
        f"*{risk_reward}*",
        f"\n🧠 {confidence}"
    ]

    return "\n".join([p for p in parts if p])
