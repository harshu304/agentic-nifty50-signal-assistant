def compute_indicators(df):
    # EMA
    df["ema_20"] = df["Close"].ewm(span=20).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    df["ema_12"] = df["Close"].ewm(span=12).mean()
    df["ema_26"] = df["Close"].ewm(span=26).mean()
    df["macd"] = df["ema_12"] - df["ema_26"]
    df["macd_signal"] = df["macd"].ewm(span=9).mean()

    return df