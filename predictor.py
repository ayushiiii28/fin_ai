import pandas as pd
import numpy as np
import xgboost as xgb

# Load model
model = xgb.XGBClassifier()
model.load_model("xgboost_model.json")

def extract_features(prices):
    df = pd.DataFrame({'Close': prices})

    df['return_1d'] = df['Close'].pct_change()
    df['volatility'] = df['Close'].rolling(window=5).std()
    df['momentum'] = df['Close'] / df['Close'].shift(5)
    df['sector_strength'] = df['Close'].rolling(window=10).mean() / df['Close']

    df.dropna(inplace=True)

    if df.empty:
        return None

    latest = df.iloc[-1]
    features = pd.DataFrame([{
        'volatility': latest['volatility'],
        'momentum': latest['momentum'],
        'sector_strength': latest['sector_strength'],
        'return_1d': latest['return_1d']
    }])

    return features

def predict_next_close(prices):
    features = extract_features(prices)

    if features is None:
        return None  # Not enough data for prediction

    prediction = model.predict_proba(features)[0][1]  # Probability of "should invest" = 1
    return float(prediction)
