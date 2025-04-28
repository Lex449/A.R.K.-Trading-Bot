# bot/utils/ultra_signal_builder.py

"""
A.R.K. Ultra Signal Builder – Premium Trade Signal Generation
Made for Ultra Precision, Risk Awareness and Dynamic Messaging.
"""

import logging
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

def build_ultra_signal(symbol: str,
                       move: dict = None,
                       volume_spike: dict = None,
                       atr_breakout: dict = None,
                       risk_reward: dict = None,
                       lang: str = "en") -> str:
    """
    Builds a premium, ultra-smart trade signal message.

    Args:
        symbol (str): Trading symbol.
        move (dict, optional): Movement alert details.
        volume_spike (dict, optional): Volume spike detection.
        atr_breakout (dict, optional): ATR breakout detection.
        risk_reward (dict, optional): Risk/Reward analysis.
        lang (str, optional): Language for output.

    Returns:
        str: Fully formatted signal message.
    """

    try:
        # === Base Header ===
        header = f"🚀 *{get_text('signal_ultra_premium', lang)}*"

        body = f"*Symbol:* `{symbol}`\n"

        # === Move Detection Info ===
        if move:
            move_type = move.get("type", "Early Move ⚡")
            move_percent = move.get("move_percent", 0.0)
            body += f"*Movement:* `{move_percent:.2f}%` – {move_type}\n"

        # === Volume Spike Info ===
        if volume_spike and volume_spike.get("volume_spike"):
            body += f"*Volume Spike:* 📈 `{volume_spike.get('volume_percent', 0):.1f}%`\n"

        # === ATR Breakout Info ===
        if atr_breakout and atr_breakout.get("atr_breakout"):
            body += "*ATR Breakout:* ✅ Confirmed\n"

        # === Risk/Reward Info ===
        if risk_reward:
            risk_reward_ratio = risk_reward.get("risk_reward_ratio", "-")
            body += f"*Risk/Reward:* `{risk_reward_ratio}:1`\n"
            body += f"*Stop-Loss:* `{risk_reward.get('stop_loss', '-')}`\n"
            body += f"*Target:* `{risk_reward.get('target', '-')}`\n"

        # === Footer ===
        footer = f"\n\n_{get_text('signal_footer', lang)}_"

        # === Full Message ===
        return f"{header}\n\n{body}{footer}"

    except Exception as e:
        logger.error(f"[Ultra Signal Builder] Error building signal: {e}")
        return f"⚠️ Error building signal for `{symbol}`."
