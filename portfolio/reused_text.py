from __future__ import annotations

import math
import re
from collections import Counter


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "by", "for",
    "from", "has", "have", "how", "i", "in", "is", "it", "of", "on",
    "or", "our", "that", "the", "this", "to", "was", "we", "what",
    "when", "which", "with", "should", "can", "current", "claim",
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9_-]+", text.lower())
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left).intersection(right)
    dot = sum(left[token] * right[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def token_f1(left: str, right: str) -> float:
    left_counts = Counter(tokenize(left))
    right_counts = Counter(tokenize(right))
    overlap = sum((left_counts & right_counts).values())
    if not overlap:
        return 0.0
    precision = overlap / max(1, sum(right_counts.values()))
    recall = overlap / max(1, sum(left_counts.values()))
    return 2 * precision * recall / (precision + recall)

