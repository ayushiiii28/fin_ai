import os
import numpy as np
import pandas as pd
import xgboost as xgb

MODEL_JSON = os.path.join(os.path.dirname(__file__), "xgboost_model.json")

MODEL_AVAILABLE = False
model = None
if os.path.exists(MODEL_JSON):
    try:
        # Try classifier first
        model = xgb.XGBClassifier()
        model.load_model(MODEL_JSON)
        MODEL_AVAILABLE = True
        MODEL_TYPE = "classifier"
    except Exception:
        try:
            # If not classifier, fallback to regressor
            model = xgb.XGBRegressor()
            model.load_model(MODEL_JSON)
            MODEL_AVAILABLE = True
            MODEL_TYPE = "regressor"
        except Exception:
            MODEL_TYPE = None
            MODEL_AVAILABLE = False


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
    return pd.DataFrame([{
        "volatility": float(last["volatility"]),
        "momentum": float(last["momentum"]),
        "sector_strength": float(last["sector_strength"]),
        "return_1d": float(last["return_1d"])
    }])


def predict_pct_from_prices(prices):
    features = extract_features_from_prices(prices)
    if features is None:
        return None

    if MODEL_AVAILABLE:
        if MODEL_TYPE == "classifier":
            proba = model.predict_proba(features)[0][1]  # probability of class 1 ("up")
            return round((proba - 0.5) * 200, 2)  # map 0.5 → 0%, 1.0 → +100%, 0.0 → -100%
        elif MODEL_TYPE == "regressor":
            return float(model.predict(features)[0])

    # fallback
    return 0.0


# ✅ Backward compatibility wrapper
def predict_next_close(prices):
    """For compatibility with old code."""
    return predict_pct_from_prices(prices)

