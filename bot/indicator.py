import pandas as pd

def compute_ema(series: pd.Series, span: int) -> pd.Series:
    """
    Berechnet den Exponential Moving Average (EMA) für eine gegebene Zeitspanne.
    """
    return series.ewm(span=span, adjust=False).mean()


def compute_rsi(series: pd.Series, period: int) -> pd.Series:
    """
    Berechnet den Relative Strength Index (RSI) für eine gegebene Periode.
    Nutzt smoothed averages für realistischere Signale.
    """
    delta = series.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
