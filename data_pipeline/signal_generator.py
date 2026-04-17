def generate_signal(df):
    if len(df) < 20:
        return "HOLD"

    latest = df.iloc[-1]

    rsi = latest["rsi"]
    macd = latest["macd"]
    signal = latest["macd_signal"]
    price = latest["Close"]
    ema = latest["ema_20"]

    # BUY logic
    if rsi < 35 and macd > signal and price > ema:
        return "BUY"

    # SELL logic
    elif rsi > 65 and macd < signal and price < ema:
        return "SELL"

    return "HOLD"