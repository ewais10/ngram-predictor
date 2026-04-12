from typing import List


class Predictor:
    """Predictor wrapper around an n-gram model."""

    def __init__(self, model):
        self.model = model

    def predict(self, context: List[str], k: int = 5) -> List[str]:
        """Return up to `k` next-token predictions (placeholder)."""
        return []
