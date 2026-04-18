def calculate_risk(price):
    return {
        "entry": round(price, 2),
        "stoploss": round(price * 0.98, 2),
        "target": round(price * 1.03, 2)
    }