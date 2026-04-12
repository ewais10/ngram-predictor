from collections import defaultdict
from typing import List


class NGramModel:
    """Simple n-gram model placeholder."""

    def __init__(self, n: int = 3):
        self.n = n
        self.counts = defaultdict(int)

    def train(self, tokens: List[str]):
        """Train on a sequence of tokens (placeholder)."""
        if not tokens:
            return
        # placeholder: count n-grams
        for i in range(len(tokens) - self.n + 1):
            gram = tuple(tokens[i : i + self.n])
            self.counts[gram] += 1
