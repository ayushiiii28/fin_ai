import numpy as np
import pickle
import os

model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

def predict_next_close(prices):
    if prices is None or len(prices) == 0:
        return None
    
    features = []
    for i in range(5, len(prices)):
        features.append(prices[i - 5:i])
    
    if not features:
        return None

    features = np.array(features)
    last_sequence = features[-1].reshape(1, -1)

    predicted_close = model.predict(last_sequence)[0]
    return predicted_close

