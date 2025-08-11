# predictor.py
import os
import numpy as np
import pandas as pd
import xgboost as xgb

MODEL_JSON = os.path.join(os.path.dirname(__file__), "xgboost_model.json")

MODEL_AVAILABLE = False
MODEL_TYPE = None
model = None

# --- Load model and detect type ---
if os.path.exists(MODEL_JSON):
    for m_type in ("classifier", "regressor"):
        try:
            if m_type == "classifier":
                temp_model = xgb.XGBClassifier()
            else:
                temp_model = xgb.XGBRegressor()
            temp_model.load_model(MODEL_JSON)
            model = temp_model
            MODEL_TYPE = m_type
            MODEL_AVAILABLE = True
            break
        except Exception:
            continue

FEATURE_NAMES = ["volatility", "momentum", "sector_strength", "return_1d"]

def extract_features_from_prices(prices):
    prices = np.array(prices).flatten()
    if len(prices) < 12:
        return None

    df = pd.DataFrame({"Close": prices})
    df["return_1d"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].rolling(window=5).std()
    df["momentum"] = df["Close"] / df["Close"].shift(5)
    df["sector_strength"] = df["Close"].rolling(window=10).mean() / df["Close"]
    df.dropna(inplace=True)

    if df.empty:
        return None

    last = df.iloc[-1]
    features = pd.DataFrame([{
        "volatility": float(last["volatility"]),
        "momentum": float(last["momentum"]),
        "sector_strength": float(last["sector_strength"]),
        "return_1d": float(last["return_1d"])
    }])

    # Ensure correct feature order & names
    features = features.reindex(columns=FEATURE_NAMES)
    return features

def predict_pct_from_prices(prices):
    features = extract_features_from_prices(prices)
    if features is None:
        return None

    if MODEL_AVAILABLE:
        if MODEL_TYPE == "classifier":
            proba = model.predict_proba(features)[0][1]
            return round((proba - 0.5) * 200, 2)  # % change scale
        elif MODEL_TYPE == "regressor":
            return round(float(model.predict(features)[0]), 2)

    # Fallback if no model
    return 0.0


