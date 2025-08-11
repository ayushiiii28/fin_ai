import pandas as pd
import numpy as np
import xgboost as xgb

# ✅ Load the trained XGBoost model
model = xgb.XGBRegressor()
model.load_model("xgboost_model.json")

def extract_features(prices):
    """Generate features from recent closing prices."""
    df = pd.DataFrame({'Close': prices})

    df["return_1d"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].rolling(window=5).std()
    df["momentum"] = df["Close"] / df["Close"].shift(5)
    df["sector_strength"] = df["Close"].rolling(window=10).mean() / df["Close"]

    # Take only the last row (latest features)
    df = df.dropna().tail(1)

    return df[["volatility", "momentum", "sector_strength", "return_1d"]]

def predict_next_close(prices):
    """Predict % gain/loss for the next day."""
    features = extract_features(prices)

    if features.empty:
        return 0  # Not enough data

    dmatrix = xgb.DMatrix(features, feature_names=features.columns)
    predicted = model.predict(dmatrix)[0]

    # Convert log-odds or raw output to percent change
    return round(predicted * 100, 2)


