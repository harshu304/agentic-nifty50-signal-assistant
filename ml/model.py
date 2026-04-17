import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def prepare_features(df):
    df = df.copy()

    # Feature engineering
    df["return"] = df["Close"].pct_change()
    df["target"] = (df["return"].shift(-1) > 0).astype(int)

    df = df.dropna()

    features = ["rsi", "macd", "ema_20"]

    X = df[features]
    y = df["target"]

    return X, y


# ✅ Train + Test Split + Evaluation
def train_model(df):
    X, y = prepare_features(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False  # time series → no shuffle
    )

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print("\n📊 Model Evaluation:")
    print(f"Accuracy: {acc:.2f}")
    print(report)

    return model


# ✅ Predict latest
def predict(model, df):
    latest = df.iloc[-1][["rsi", "macd", "ema_20"]]
    latest_df = latest.to_frame().T

    pred = model.predict(latest_df)[0]

    return "BUY" if pred == 1 else "SELL"