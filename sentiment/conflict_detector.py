def detect_conflict(signal, sentiment):
    if signal == "BUY" and sentiment == "NEGATIVE":
        return True
    if signal == "SELL" and sentiment == "POSITIVE":
        return True
    return False