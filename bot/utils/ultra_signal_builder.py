"""
A.R.K. Ultra Signal Builder – Hyper Precision Trade Signal Generation
Built for Deep Confidence, Dynamic Risk Profiling, and Adaptive Messaging.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def build_ultra_signal(
    symbol: str,
    move: dict | str = None,
    volume_spike: dict = None,
    atr_breakout: dict = None,
    risk_reward: dict = None,
    confidence: float = None,
    lang: str = "en"
) -> str:
    """
    Builds a multilingual ultra-intelligent trading signal message.

    Args:
        symbol (str): Trading symbol (e.g., AAPL)
        move (dict|str): Movement info or summary
        volume_spike (dict): Volume info from detector
        atr_breakout (dict): ATR breakout info
        risk_reward (dict): RRR output
        confidence (float): Signal confidence
        lang (str): Language code (en or de)

    Returns:
        str: Formatted signal message
    """
    try:
        # === Header ===
        header = f"🚀 *{get_text('signal_ultra_premium', lang)}*\n"

        # === Core Body ===
        body = f"*Symbol:* `{symbol}`\n"

        # === Move Detection ===
        if move:
            if isinstance(move, dict):
                move_type = move.get("type", get_text("move_detected", lang))
                move_percent = move.get("move_percent", 0.0)
                body += f"*Move:* `{move_percent:.2f}%` – {move_type}\n"
            elif isinstance(move, str):
                body += f"*Move:* `{move}`\n"

        # === Volume Spike ===
        if volume_spike and volume_spike.get("volume_spike", False):
            volume_pct = volume_spike.get("volume_percent", 0.0)
            body += f"*Volume Spike:* `{volume_pct:.1f}%` 📈\n"

        # === ATR Breakout ===
        if atr_breakout and atr_breakout.get("atr_breakout", False):
            body += f"*ATR Breakout:* ✅ {get_text('confirmed', lang)}\n"

        # === Risk/Reward Output ===
        if risk_reward:
            rr = risk_reward.get("risk_reward_ratio", "-")
            sl = risk_reward.get("stop_loss", "-")
            tgt = risk_reward.get("target", "-")
            body += (
                f"*Risk/Reward:* `{rr}:1`\n"
                f"*Stop-Loss:* `{sl}`\n"
                f"*Target:* `{tgt}`\n"
            )

        # === Confidence ===
        if confidence is not None:
            body += f"*Confidence:* `{confidence:.1f}%`\n"

        # === Footer ===
        footer = f"\n_{get_text('signal_footer', lang)}_"

        return f"{header}\n{body}{footer}"

    except Exception as e:
        logger.error(f"❌ [UltraSignalBuilder] Signal build failed for {symbol}: {e}")
        return f"⚠️ Error building signal for `{symbol}`."
