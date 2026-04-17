import yfinance as yf

def fetch_market_data(ticker, interval="5m"):
    df = yf.download(
        ticker,
        period="1d",
        interval=interval,
        progress=False
    )

    if df.empty:
        return None

    # Fix multi-index columns
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    return df.dropna()