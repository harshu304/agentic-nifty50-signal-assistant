from fastapi import FastAPI
from data_pipeline.market_fetcher import fetch_market_data
from data_pipeline.indicators import compute_indicators
from data_pipeline.signal_generator import generate_signal

app = FastAPI()

@app.get("/signal/{ticker}")
def get_signal(ticker: str):
    df = fetch_market_data(ticker)

    if df is None:
        return {"error": "No data"}

    df = compute_indicators(df)
    signal = generate_signal(df)

    return {
        "stock": ticker,
        "price": float(df["Close"].iloc[-1]),
        "signal": signal
    }