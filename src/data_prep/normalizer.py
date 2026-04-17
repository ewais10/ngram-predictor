from importlib_metadata import files
from pathlib import Path
from typing import Dict
import re

class Normalizer:
    """The Normalizer class handles loading, cleaning, tokenizing, and saving the corpus."""

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
    
    def strip_gutenberg(text: str):
        """Strip Gutenberg header and footer from text."""
        reTextStart = re.search("\*\*\*\ START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)
        reTextEnd = re.search("\*\*\*\ END OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)

        gbStartIndex = reTextStart.span()[1] + 1
        gbEndIndex = reTextEnd.span()[0] - 1

        print(f"Gutenberg header ends at index: {gbStartIndex} and footer starts at index: {gbEndIndex}")
        text = text[gbStartIndex:gbEndIndex]
        return text;

    # def strip_gutenberg(text):
    #     """Strip Gutenberg header and footer from text."""
    #     if text is None:
    #         return ""
    #     lines = text.splitlines()
    #     start_idx = 0
    #     end_idx = len(lines)
    #     for i, line in enumerate(lines):
    #         if line.startswith("*** START OF THIS PROJECT GUTENBERG EBOOK"):
    #             start_idx = i + 1
    #             break
    #     for i in range(len(lines)-1, -1, -1):
    #         if lines[i].startswith("*** END OF THIS PROJECT GUTENBERG EBOOK"):
    #             end_idx = i
    #             break
    #     return "\n".join(lines[start_idx:end_idx])

if __name__ == "__main__":
    # Example usage
    dataN = Normalizer.load("data/raw/train")
    print(f"Loaded {len(dataN)} files.")
    print(dataN.keys())
    y=(dataN['data\\raw\\train\\108.txt'])
    newText = Normalizer.strip_gutenberg(y)
    print(newText)
    # print(Normalizer.__doc__)
    # # help(Normalizer.load)