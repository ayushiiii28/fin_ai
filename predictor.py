import numpy as np
import pandas as pd
import xgboost as xgb
import os

# Load the XGBoost model (must be JSON if saved with save_model)
model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.json")
model = xgb.Booster()
model.load_model(model_path)

def extract_features(prices: np.ndarray) -> xgb.DMatrix:
    df = pd.DataFrame({'Close': prices})
    df["return_1d"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].rolling(window=5).std()
    df["momentum"] = df["Close"] / df["Close"].shift(5)
    df["sector_strength"] = df["Close"].rolling(window=10).mean() / df["Close"]
    features = df[["volatility", "momentum", "sector_strength", "return_1d"]].dropna().iloc[-1:]
    return xgb.DMatrix(features)

def predict_next_close(prices):
    if len(prices) < 10:
        return 0  # Not enough data

    prices = np.array(prices)
    dmatrix = extract_features(prices)
    prediction = model.predict(dmatrix)[0]  # Probability output
    return int(prediction >= 0.5)  # Return 1 if invest, else 0

