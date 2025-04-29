"""
A.R.K. Ultra Signal Builder – Hyper Precision Trade Signal Generation
Built for Deep Confidence, Dynamic Risk Profiling, and Adaptive Messaging.
"""

from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

def build_ultra_signal(symbol: str,
                       move=None,
                       volume_spike: dict = None,
                       atr_breakout: dict = None,
                       risk_reward: dict = None,
                       confidence: float = None,
                       lang: str = "en") -> str:
    """
    Builds a premium, ultra-intelligent trading signal message.
    """

    try:
        # === Header ===
        header = f"🚀 *{get_text('signal_ultra_premium', lang)}*"

        # === Main Body ===
        body = f"*Symbol:* `{symbol}`\n"

        # === Movement Detection ===
        if move:
            if isinstance(move, dict):
                move_type = move.get("type", "Early Move ⚡")
                move_percent = move.get("move_percent", 0.0)
                body += f"*Movement:* `{move_percent:.2f}%` – {move_type}\n"
            elif isinstance(move, str):
                body += f"*Move:* `{move}`\n"

        # === Volume Spike ===
        if volume_spike and volume_spike.get("volume_spike"):
            volume_percent = volume_spike.get("volume_percent", 0.0)
            body += f"*Volume Spike:* 📈 `{volume_percent:.1f}%`\n"

        # === ATR Breakout ===
        if atr_breakout and atr_breakout.get("atr_breakout"):
            body += "*ATR Breakout:* ✅ Confirmed\n"

        # === Risk-Reward ===
        if risk_reward:
            rr_ratio = risk_reward.get("risk_reward_ratio", "-")
            stop_loss = risk_reward.get("stop_loss", "-")
            target = risk_reward.get("target", "-")
            body += (
                f"*Risk/Reward:* `{rr_ratio}:1`\n"
                f"*Stop-Loss:* `{stop_loss}`\n"
                f"*Target:* `{target}`\n"
            )

        # === Confidence Score ===
        if confidence is not None:
            body += f"*Confidence:* `{confidence:.1f}%`\n"

        # === Footer ===
        footer = f"\n\n_{get_text('signal_footer', lang)}_"

        return f"{header}\n\n{body}{footer}"

    except Exception as e:
        logger.error(f"[Ultra Signal Builder] Error building signal for {symbol}: {e}")
        return f"⚠️ Error building signal for `{symbol}`."
