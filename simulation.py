# simulation.py
import math
import numpy as np
import yfinance as yf
from predictor import predict_probability
from allocator import allocate_funds

# Tunable weights
W_PROB = 0.6      # weight for model probability
W_RISK = 0.25     # weight for inverse volatility (low vol -> higher score)
W_QUALITY = 0.15  # weight for company quality (market cap)

MIN_ALLOC_PCT = 0.02  # minimum allocation pct per stock (2%), optional floor

def get_market_cap(ticker):
    try:
        info = yf.Ticker(ticker).info
        mc = info.get("marketCap") or info.get("market_cap") or 0
        return float(mc) if mc else 0.0
    except Exception:
        return 0.0

def compute_inv_volatility(close_series):
    # compute daily returns and 20-day std (or fallback)
    returns = np.array(close_series).flatten()
    if len(returns) < 5:
        return 0.0
    pct = np.diff(returns) / returns[:-1]
    vol = np.std(pct[-20:]) if len(pct) >= 20 else np.std(pct)
    if math.isnan(vol) or vol <= 0:
        return 0.0
    return 1.0 / vol

def simulate_investment(amount, tickers):
    raw_scores = {}
    details = {}

    # gather base info
    market_caps = {}
    for t in tickers:
        market_caps[t] = get_market_cap(t)

    # normalize market cap (log scale)
    caps = np.array([market_caps[t] for t in tickers], dtype=float)
    # avoid log(0)
    caps_log = np.log1p(caps)
    cap_min, cap_max = caps_log.min() if len(caps_log)>0 else 0, caps_log.max() if len(caps_log)>0 else 1
    cap_range = cap_max - cap_min if cap_max != cap_min else 1.0

    for t in tickers:
        try:
            df = yf.download(t, period="60d", interval="1d", progress=False, auto_adjust=True)
        except Exception as e:
            details[t] = {"error": f"data fetch failed: {e}"}
            raw_scores[t] = 0.0
            continue

        if df is None or df.empty or "Close" not in df:
            details[t] = {"error": "no data"}
            raw_scores[t] = 0.0
            continue

        close_vals = df["Close"].values
        prob = predict_probability(close_vals)
        if prob is None:
            prob = 0.0

        inv_vol = compute_inv_volatility(close_vals)  # could be large
        # normalize inverse volatility across tickers later; store raw for now
        quality = 0.0
        # normalize market cap log to [0,1]
        if cap_range > 0:
            q = (math.log1p(market_caps[t]) - cap_min) / cap_range
            quality = float(max(0.0, min(1.0, q)))
        else:
            quality = 0.0

        details[t] = {
            "probability": round(prob, 4),
            "inv_vol": float(inv_vol),
            "market_cap": market_caps[t],
            "quality": round(quality, 4)
        }
        raw_scores[t] = {"prob": prob, "inv_vol": inv_vol, "quality": quality}

    # Normalize inv_vol to 0..1 across tickers
    inv_vals = np.array([raw_scores[t]["inv_vol"] for t in tickers], dtype=float)
    inv_min, inv_max = inv_vals.min() if len(inv_vals)>0 else 0.0, inv_vals.max() if len(inv_vals)>0 else 1.0
    inv_range = inv_max - inv_min if inv_max != inv_min else 1.0

    # Build final combined scores
    combined = {}
    for t in tickers:
        prob = raw_scores[t]["prob"]
        inv_v = raw_scores[t]["inv_vol"]
        quality = raw_scores[t]["quality"]

        inv_norm = (inv_v - inv_min) / inv_range if inv_range > 0 else 0.0
        # final score is weighted sum
        score = W_PROB * prob + W_RISK * inv_norm + W_QUALITY * quality
        # ensure non-negative
        score = max(0.0, score)
        combined[t] = score
        details[t].update({"inv_norm": round(inv_norm, 4), "combined": round(score, 6)})

    # apply minimum allocation floor: give each at least MIN_ALLOC_PCT of amount proportionally from combined scores
    # convert to raw allocation weights
    weights = combined.copy()
    # if all zeros, leave zero allocations
    total_weight = sum(weights.values())
    if total_weight == 0:
        allocations = {t: 0.0 for t in tickers}
        return allocations, details

    # first compute allocations proportional to weights
    allocations = {t: (weights[t] / total_weight) * amount for t in tickers}

    # apply minimum floor
    min_amount = MIN_ALLOC_PCT * amount
    needy = [t for t in tickers if allocations[t] < min_amount]
    if needy:
        # amount needed to raise each to min
        needed = sum(max(0, min_amount - allocations[t]) for t in needy)
        # reduce from those > min_amount proportionally
        donors = [t for t in tickers if allocations[t] > min_amount]
        donor_total = sum(allocations[t] - min_amount for t in donors) if donors else 0
        if donor_total > 0:
            for t in donors:
                reduce_amt = ((allocations[t] - min_amount) / donor_total) * needed
                allocations[t] -= reduce_amt
            for t in needy:
                allocations[t] = min_amount
        else:
            # can't satisfy floors, leave original allocations
            pass

    # round allocations
    allocations = {t: round(float(allocations[t]), 2) for t in tickers}

    return allocations, details

