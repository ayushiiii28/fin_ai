import pandas as pd
import numpy as np
import xgboost as xgb
import os
import pickle

# ✅ Load model using XGBClassifier to retain feature names
model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.json")
model = xgb.XGBClassifier()
model.load_model(model_path)

def predict_next_close(prices):
    if prices is None or len(prices) < 10:
        return float(prices[-1]) if len(prices) > 0 else 0.0

    prices = np.array(prices).flatten()
    recent = prices[-6:]
    returns = (recent[1:] - recent[:-1]) / recent[:-1]

    volatility = float(np.std(returns))
    momentum = float(prices[-1] / prices[-6])
    sector_strength = float(np.mean(prices[-10:]) / prices[-1])
    last_return = float(returns[-1])

    # ✅ Create DataFrame with expected feature names
    features_df = pd.DataFrame([{
        "volatility": volatility,
        "momentum": momentum,
        "sector_strength": sector_strength,
        "return_1d": last_return
    }])

    # ✅ Predict directly using the classifier
    predicted = model.predict(features_df)[0]
    return float(predicted)

