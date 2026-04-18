import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

import numpy as np
import pandas as pd

def prepare_features(df):
    df = df.copy()

    # ==============================
    # Feature Engineering
    # ==============================
    df["return"] = df["Close"].pct_change()

    # Better target (avoid noise)
    df["target"] = (df["return"].shift(-1) > 0.002).astype(int)

    df["volume_change"] = df["Volume"].pct_change()
    df["price_change"] = df["Close"].pct_change()

    # Lag features
    df["rsi_lag1"] = df["rsi"].shift(1)
    df["macd_lag1"] = df["macd"].shift(1)

    # ==============================
    # 🚨 FIX: Handle inf values
    # ==============================
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df = df.dropna()

    features = [
        "rsi", "macd", "ema_20",
        "volume_change", "price_change",
        "rsi_lag1", "macd_lag1"
    ]

    X = df[features]
    y = df["target"]

    return X, y, features


# ==============================
# 🤖 TRAIN + EVALUATE
# ==============================
def train_model(df):
    X, y, features = prepare_features(df)

    # Time-series split (no shuffle)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print("\n📊 Model Evaluation:")
    print(f"Accuracy: {acc:.2f}")
    print(report)

    return model, features


# ==============================
# 🔮 PREDICT (LATEST DATA)
# ==============================
def predict(model, df, features):
    df = df.copy()

    # Recompute same features (IMPORTANT)
    df["volume_change"] = df["Volume"].pct_change()
    df["price_change"] = df["Close"].pct_change()
    df["rsi_lag1"] = df["rsi"].shift(1)
    df["macd_lag1"] = df["macd"].shift(1)

    df = df.dropna()

    latest = df.iloc[-1][features]
    latest_df = latest.to_frame().T

    pred = model.predict(latest_df)[0]

    return "BUY" if pred == 1 else "SELL"