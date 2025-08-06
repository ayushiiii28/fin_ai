import numpy as np
import pandas as pd
import xgboost as xgb

# Load model from JSON
model = xgb.XGBClassifier()
model.load_model("xgboost_model.json")

def extract_features(prices):
    prices = np.array(prices).flatten()  # ✅ Ensure it's 1D
    df = pd.DataFrame({'Close': prices})

    # Feature engineering
    df['return_1d'] = df['Close'].pct_change()
    df['volatility'] = df['Close'].rolling(window=5).std()
    df['momentum'] = df['Close'] / df['Close'].shift(5)
    df['sector_strength'] = df['Close'].rolling(window=10).mean() / df['Close']

    # Drop NaNs caused by rolling calculations
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
        return "Insufficient data"
    dmatrix = xgb.DMatrix(features, feature_names=features.columns.tolist())
    predicted = model.predict(features)[0]
    return predicted

