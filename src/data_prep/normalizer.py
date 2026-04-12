class Normalizer:
    """Simple text normalizer placeholder."""

    def normalize(self, text: str) -> str:
        """Normalize text to lower-case and strip whitespace."""
        if text is None:
            return ""
        return text.strip().lower()
