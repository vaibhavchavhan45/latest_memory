def estimate_tokens(text: str) -> int:
    # simple heuristic: ~4 chars per token
    return max(1, len(text) // 4)
