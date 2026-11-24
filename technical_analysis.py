
import pandas as pd
import yfinance as yf


def fetch_history(symbol, period="1y", interval="1d"):
    """
    Download historical OHLCV market data.
    Examples:
    BTC-USD, ETH-USD, AAPL, GC=F, SI=F,
    EURUSD=X, ^GSPC
    """

    try:
        data = yf.Ticker(symbol).history(
            period=period,
            interval=interval,
            auto_adjust=True
        )

        if data.empty:
            return None

        required = ["Open", "High", "Low", "Close", "Volume"]

        if not all(column in data.columns for column in required):
            return None

        return data[required].dropna()

    except Exception as error:
        print(f"Data error for {symbol}: {error}")
        return None


def calculate_indicators(data):
    if data is None or len(data) < 50:
        return None

    df = data.copy()

    # Exponential moving averages
    df["EMA20"] = df["Close"].ewm(
        span=20, adjust=False
    ).mean()

    df["EMA50"] = df["Close"].ewm(
        span=50, adjust=False
    ).mean()

    # RSI (14)
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / 14,
        adjust=False,
        min_periods=14
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / 14,
        adjust=False,
        min_periods=14
    ).mean()

    rs = avg_gain / avg_loss.replace(0, float("nan"))

    df["RSI"] = 100 - (100 / (1 + rs))

    df.loc[
        (avg_loss == 0) & (avg_gain > 0),
        "RSI"
    ] = 100

    df.loc[
        (avg_gain == 0) & (avg_loss > 0),
        "RSI"
    ] = 0

    # MACD
    ema12 = df["Close"].ewm(
        span=12, adjust=False
    ).mean()

    ema26 = df["Close"].ewm(
        span=26, adjust=False
    ).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_signal"] = df["MACD"].ewm(
        span=9, adjust=False
    ).mean()

    df["MACD_histogram"] = (
        df["MACD"] - df["MACD_signal"]
    )

    return df.dropna()


def generate_signal(data):
    if data is None or len(data) < 2:
        return {"signal": "NO_DATA"}

    latest = data.iloc[-1]

    price = float(latest["Close"])
    rsi = float(latest["RSI"])
    ema20 = float(latest["EMA20"])
    ema50 = float(latest["EMA50"])
    macd = float(latest["MACD"])
    macd_signal = float(latest["MACD_signal"])

    bullish = (
        ema20 > ema50
        and macd > macd_signal
        and 50 <= rsi < 70
    )

    bearish = (
        ema20 < ema50
        and macd < macd_signal
        and 30 < rsi <= 50
    )

    if bullish:
        signal = "BUY"
    elif bearish:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "price": round(price, 4),
        "RSI": round(rsi, 2),
        "EMA20": round(ema20, 4),
        "EMA50": round(ema50, 4),
        "MACD": round(macd, 4),
        "MACD_signal": round(macd_signal, 4)
    }


def analyze_market(symbol):
    history = fetch_history(symbol)

    if history is None:
        return {
            "symbol": symbol,
            "signal": "NO_DATA",
            "error": "Market data unavailable"
        }

    indicators = calculate_indicators(history)

    if indicators is None or indicators.empty:
        return {
            "symbol": symbol,
            "signal": "NO_DATA",
            "error": "Not enough historical data"
        }

    result = generate_signal(indicators)
    result["symbol"] = symbol

    return result


if __name__ == "__main__":

    symbols = [
        "BTC-USD",
        "ETH-USD",
        "GC=F",
        "SI=F",
        "EURUSD=X",
        "AAPL",
        "^GSPC"
    ]

    for symbol in symbols:
        result = analyze_market(symbol)
        print(result)
