def greedy_rank(rec_stats, k=5):
    """
    rec_stats: list of (rid, matched_list, missing_list, ratio)
    returns top-k dicts with summary
    """
    out = []
    for rid, matched, missing, ratio in rec_stats:
        out.append({
            "id": rid,
            "matched": matched,
            "missing": missing,
            "ratio": ratio
        })
    return out[:k]
