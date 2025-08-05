# allocator.py

def allocate_funds(predictions, total_investment):
    """
    Allocate funds proportionally to prediction scores.
    Returns a dictionary with asset: amount_allocated
    """
    total_score = sum(predictions.values())

    allocations = {}
    for asset, score in predictions.items():
        allocation = (score / total_score) * total_investment if total_score > 0 else 0
        allocations[asset] = round(allocation, 2)
    return allocations
