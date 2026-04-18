def llm_decision_node(state):
    ml_signal = state["ml_signal"]
    sentiment = state["sentiment"]

    # Simple reasoning (later replace with real LLM API)
    if ml_signal == "BUY" and sentiment != "NEGATIVE":
        decision = "BUY"
    elif ml_signal == "SELL" and sentiment != "POSITIVE":
        decision = "SELL"
    else:
        decision = "HOLD"

    state["decision"] = decision
    return state