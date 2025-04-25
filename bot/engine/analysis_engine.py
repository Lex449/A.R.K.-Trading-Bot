import os
import asyncio
from twelvedata import TDClient
from bot.config.settings import get_settings

# Konfiguration laden
settings = get_settings()

# Überprüfen, ob der API-Schlüssel gesetzt ist
TD_API_KEY = settings.get("TWELVEDATA_API_KEY")
if not TD_API_KEY:
    raise ValueError("TWELVEDATA_API_KEY is missing.")

# Initialisierung des TwelveData Clients
td = TDClient(apikey=TD_API_KEY)

async def fetch_data(symbol: str) -> list:
    """Holt historische Kursdaten von TwelveData."""
    try:
        # Hole Zeitreihendaten vom TwelveData API
        series = td.time_series(
            symbol=symbol,
            interval=settings["INTERVAL"],  # 1-Minuten-Intervall
            outputsize=50  # Maximale Anzahl der abgerufenen Datenpunkte
        ).as_json()

        # Überprüfen des Typs der zurückgegebenen Daten
        if isinstance(series, dict) and "values" in series:
            print(f"[DEBUG] Rohantwort für {symbol}: {series}")  # Ausgabe der Antwort für Debugging
            return series["values"]
        else:
            print(f"[ERROR] Unerwartetes Datenformat für {symbol}: {series}")
            return []

    except Exception as e:
        print(f"[ERROR] Datenabruf fehlgeschlagen für {symbol}: {e}")
        return []

async def analyze_symbol(symbol: str):
    """Analysiert das Symbol und gibt das Signal zurück."""
    # Holen der Kursdaten
    data = await asyncio.to_thread(fetch_data, symbol)  # Async-Funktion korrekt verwenden
    
    if not data or len(data) < 20:
        return f"❌ No sufficient data for {symbol}."

    # Extrahieren der Schlusskurse
    closes = [float(entry["close"]) for entry in reversed(data)]
    
    # Berechnungen
    rsi = calculate_rsi(closes)
    ema_short = calculate_ema(closes, period=settings["EMA_SHORT_PERIOD"])
    ema_long = calculate_ema(closes, period=settings["EMA_LONG_PERIOD"])
    trend = detect_trend(ema_short, ema_long)
    sideways = detect_sideways(closes)
    stars = generate_stars(rsi, trend, sideways)

    return {
        "price": closes[-1],  # Letzter Schlusskurs
        "signal": "BUY" if trend == "up" else "SELL",  # Signal basierend auf dem Trend
        "rsi": rsi,
        "trend": trend,
        "pattern": "bullish" if trend == "up" else "bearish",  # Muster basierend auf dem Trend
        "stars": stars  # Sternebewertung
    }

def calculate_rsi(prices: list, period: int = 14) -> float:
    """Berechnet den RSI (Relative Strength Index) eines Preisverlaufs."""
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))  # Gewinne
        losses.append(max(-diff, 0))  # Verluste
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def calculate_ema(prices: list, period: int) -> float:
    """Berechnet den Exponential Moving Average (EMA) eines Preisverlaufs."""
    ema = sum(prices[:period]) / period
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return round(ema, 2)

def detect_trend(ema_short: float, ema_long: float) -> str:
    """Erkennt den Trend basierend auf den EMA-Schnitten."""
    if ema_short > ema_long:
        return "up"
    elif ema_short < ema_long:
        return "down"
    return "neutral"

def detect_sideways(prices: list, threshold: float = 0.01) -> bool:
    """Erkennt einen Seitwärtstrend basierend auf den Preisabweichungen."""
    min_price = min(prices[-20:])
    max_price = max(prices[-20:])
    return (max_price - min_price) / min_price < threshold

def generate_stars(rsi: float, trend: str, sideways: bool) -> int:
    """Generiert eine Sternebewertung basierend auf RSI, Trend und Seitwärtsbewegung."""
    stars = 3  # Basisbewertung
    if sideways:
        return stars  # Seitwärtstrend bleibt bei 3 Sternen
    if trend == "up":
        stars += 1  # Trend nach oben = mehr Sterne
    elif trend == "down":
        stars -= 1  # Trend nach unten = weniger Sterne
    if rsi < 30:
        stars += 1  # RSI < 30 = Überverkauf = mehr Sterne
    elif rsi > 70:
        stars -= 1  # RSI > 70 = Überkauft = weniger Sterne
    return min(max(stars, 1), 5)  # Sterne müssen zwischen 1 und 5 liegen
