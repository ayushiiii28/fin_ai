# predictor.py
import numpy as np
import pandas as pd
import xgboost as xgb
import os

# Load trained classifier (JSON saved by model.save_model)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgboost_model.json")
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

def extract_features(prices):
    """Return a 1-row DataFrame with the features used by the model."""
    prices = np.array(prices).flatten()
    if len(prices) < 12:
        return None

    df = pd.DataFrame({"Close": prices})
    df['return_1d'] = df['Close'].pct_change()
    df['volatility'] = df['Close'].rolling(window=5).std()
    df['momentum'] = df['Close'] / df['Close'].shift(5)
    df['sector_strength'] = df['Close'].rolling(window=10).mean() / df['Close']
    df = df.dropna()
    if df.empty:
        return None

    last = df.iloc[-1]
    features = pd.DataFrame([{
        "volatility": last["volatility"],
        "momentum": last["momentum"],
        "sector_strength": last["sector_strength"],
        "return_1d": last["return_1d"]
    }])
    return features

def predict_probability(prices):
    """
    Returns probability (float) that next-day close > today (model's positive class prob).
    Returns None if insufficient data.
    """
    features = extract_features(prices)
    if features is None:
        return None
    # model.predict_proba expects DataFrame with correct column names
    prob = model.predict_proba(features)[0][1]
    return float(prob)

