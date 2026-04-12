from importlib_metadata import files
from pathlib import Path
from typing import Dict

class Normalizer:
    """Simple text normalizer placeholder."""

    def normalize(self, text: str) -> str:
        """Normalize text to lower-case and strip whitespace."""
        if text is None:
            return ""
        return text.strip().lower()

    def load(folder: str | Path,  encoding: str = "utf-8") -> Dict[str, str]:
        """Load all .txt files from a folder in a dictionary."""
        p = Path(folder)
        files = p.rglob("*.txt")
        texts: Dict[str, str] = {}
        for f in files: 
            if f.is_file:
                try:
                    texts[str(f)] = f.read_text(encoding=encoding)
                    # print(str(f)); ## For debugging
                except Exception as e:
                    print(f"Warning: failed to read {f}: {e}")
        return texts