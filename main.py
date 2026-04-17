from data_pipeline.market_fetcher import fetch_market_data
from data_pipeline.indicators import compute_indicators
from ml.model import train_model, predict
from data_pipeline.news_fetcher import fetch_news
from sentiment.finbert_analyzer import analyze_sentiment
from agent.graph import run_agent

import pandas as pd

# 🔥 NIFTY 50 (start small for speed)
NIFTY50 = [
    "RELIANCE.NS",
    "INFY.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

print("\n🚀 Starting NIFTY50 AI Signal Engine...\n")

# ==============================
# ✅ STEP 1: TRAIN MODEL (ONCE)
# ==============================

print("📊 Training ML model on sample stock...\n")

df_sample = fetch_market_data("INFY.NS")

if df_sample is None:
    raise Exception("❌ Failed to fetch training data")

df_sample = compute_indicators(df_sample)

model = train_model(df_sample)

print("\n✅ Model training completed\n")

# ==============================
# ✅ STEP 2: SCAN ALL STOCKS
# ==============================

results = []

for stock in NIFTY50:
    print(f"\n🔍 Processing {stock}...")

    df = fetch_market_data(stock)

    if df is None:
        print("❌ No data, skipping...")
        continue

    df = compute_indicators(df)

    # ==============================
    # 🤖 ML Prediction
    # ==============================
    ml_signal = predict(model, df)

    # ==============================
    # 📰 News + Sentiment
    # ==============================
    headlines = fetch_news(stock)
    sentiment = analyze_sentiment(headlines)

    # ==============================
    # 🧠 Agent Decision (LLM Logic)
    # ==============================
    state = {
        "stock": stock,
        "ml_signal": ml_signal,
        "sentiment": sentiment
    }

    final = run_agent(state)

    # ==============================
    # 💰 Price + Risk
    # ==============================
    price = float(df["Close"].iloc[-1])

    stoploss = round(price * 0.98, 2)
    target = round(price * 1.03, 2)

    # ==============================
    # 📊 Store Results
    # ==============================
    results.append({
        "stock": stock,
        "price": price,
        "ml_signal": ml_signal,
        "sentiment": sentiment,
        "final_decision": final["decision"],
        "stoploss": stoploss,
        "target": target
    })

    # ==============================
    # 🖥️ Print Output
    # ==============================
    print(f"💰 Price: {price}")
    print(f"🤖 ML Signal: {ml_signal}")
    print(f"📰 Sentiment: {sentiment}")
    print(f"🧠 Final Decision: {final['decision']}")
    print(f"🛑 Stoploss: {stoploss} | 🎯 Target: {target}")

# ==============================
# 📈 FINAL SUMMARY
# ==============================

df_results = pd.DataFrame(results)

print("\n📊 FINAL RESULTS:\n")
print(df_results)

# ==============================
# 📊 SIGNAL COUNTS
# ==============================

buy_count = (df_results["final_decision"] == "BUY").sum()
sell_count = (df_results["final_decision"] == "SELL").sum()
hold_count = (df_results["final_decision"] == "HOLD").sum()

print("\n📊 SIGNAL SUMMARY:")
print(f"✅ BUY: {buy_count}")
print(f"❌ SELL: {sell_count}")
print(f"⏸️ HOLD: {hold_count}")