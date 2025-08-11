# allocator.py
def allocate_funds_from_scores(scores: dict, total_amount: float, min_alloc_pct=0.02):
    # scores: dict[ticker] = score>=0
    total = sum(scores.values())
    if total <= 0:
        return {k: 0.0 for k in scores}
    raw = {k: (scores[k] / total) * total_amount for k in scores}
    # apply min allocation similarly as above (omitted for brevity)
    return raw
