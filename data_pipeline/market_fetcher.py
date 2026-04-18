import yfinance as yf

def fetch_market_data(ticker, interval="5m"):
    
    # 🔥 Fix: choose correct period based on interval
    if interval == "5m":
        period = "60d"
    elif interval == "1m":
        period = "7d"
    else:
        period = "1y"

    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False
    )

    if df.empty:
        return None

    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    return df.dropna()