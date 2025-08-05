import numpy as np  # ✅ This is the missing line
import pickle
import os

model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

def predict_next_close(prices):
    if prices is None or len(prices) < 4:
        return None
    
    prices = np.array(prices)

    features = []
    for i in range(4, len(prices)):
        features.append(prices[i - 4:i])

    if not features:
        return None

    features = np.array(features)
    last_sequence = features[-1].reshape(1, -1)

    predicted_close = model.predict(last_sequence)[0]
    return round(float(predicted_close), 2)
